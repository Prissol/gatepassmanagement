# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class MaterialPassLine(models.Model):
    _name = 'gate.material.pass.line'
    _description = 'Material Gate Pass Line'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    pass_id = fields.Many2one('gate.material.pass', string='Gate Pass', required=True, ondelete='cascade', index=True)
    item_name = fields.Char(string='Item Description', required=True)
    item_code = fields.Char(string='Item Code')
    quantity = fields.Float(string='Quantity', required=True, default=1.0, digits=(16, 3))
    uom = fields.Char(string='Unit of Measure', default='Pcs')
    serial_number = fields.Char(string='Serial Number')
    remarks = fields.Text(string='Remarks')

    @api.constrains('quantity')
    def _check_quantity(self):
        """Validate that quantity is greater than zero."""
        for record in self:
            if record.quantity <= 0:
                raise ValidationError(_('Quantity must be greater than zero.'))


class MaterialPass(models.Model):
    _name = 'gate.material.pass'
    _description = 'Material Gate Pass'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(string='Gate Pass Number', required=True, readonly=True, copy=False, default=lambda self: _('New'), index=True)
    date = fields.Datetime(string='Request Date', required=True, default=fields.Datetime.now, tracking=True,
                           help='Date and time when the gate pass request was created')
    requester_id = fields.Many2one('res.users', string='Requested By', required=True, 
                                   default=lambda self: self.env.user, tracking=True, index=True,
                                   help='User who is requesting this material gate pass')
    requester_email = fields.Char(related='requester_id.email', string='Requester Email', readonly=True,
                                 help='Email address of the person requesting this gate pass')
    requester_phone = fields.Char(related='requester_id.phone', string='Requester Phone', readonly=True,
                                 help='Phone number of the person requesting this gate pass')
    department_id = fields.Many2one('hr.department', string='Department', required=True, tracking=True, index=True,
                                   help='Department requesting the material gate pass')
    material_lines = fields.One2many('gate.material.pass.line', 'pass_id', string='Material Items', required=True)
    purpose = fields.Text(string='Purpose of Movement', required=True, tracking=True,
                         help='Detailed description of why the materials are being moved')
    movement_type = fields.Selection([
        ('out', 'Material Outgoing'),
        ('in', 'Material Incoming'),
        ('return', 'Material Return'),
        ('transfer', 'Internal Transfer')
    ], string='Movement Type', required=True, default='out', tracking=True,
       help='Type of material movement: Outgoing (materials leaving), Incoming (materials entering), Return (materials being returned), or Internal Transfer')
    vehicle_no = fields.Char(string='Vehicle Registration Number', tracking=True,
                            help='Vehicle registration number that will transport the materials')
    driver_name = fields.Char(string='Driver Name', tracking=True,
                             help='Name of the driver who will transport the materials')
    driver_license = fields.Char(string='Driver License Number', tracking=True,
                                help='Driver license number for identification purposes')
    driver_phone = fields.Char(string='Driver Contact Number', tracking=True,
                              help='Contact phone number of the driver')
    expected_return_date = fields.Datetime(string='Expected Return Date', tracking=True,
                                          help='Expected date and time when the materials will be returned (for outgoing materials)')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True, index=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency', readonly=True)
    attachment = fields.Binary(string='Supporting Documents', attachment=True,
                              help='Upload supporting documents related to this gate pass (e.g., approval letters, invoices)')
    attachment_filename = fields.Char(string='Attachment Filename')
    notes = fields.Text(string='Internal Notes', help='Internal notes visible only to authorized personnel')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('out', 'Gate Out'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True, tracking=True)
    
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True, tracking=True,
                                 help='User who approved this gate pass')
    approved_date = fields.Datetime(string='Approval Date & Time', readonly=True, tracking=True,
                                    help='Date and time when this gate pass was approved')
    gate_officer_id = fields.Many2one('res.users', string='Gate Officer', tracking=True,
                                      help='Gate officer who processed this gate pass at the gate')
    out_date = fields.Datetime(string='Gate Out Date & Time', readonly=True, tracking=True,
                              help='Actual date and time when materials left the gate')
    returned_date = fields.Datetime(string='Return Date & Time', readonly=True, tracking=True,
                                   help='Actual date and time when materials were returned')
    total_items = fields.Integer(string='Total Items', compute='_compute_total_items', store=True,
                                help='Total number of material items in this gate pass')
    
    @api.constrains('expected_return_date', 'date')
    def _check_return_date(self):
        """Validate that expected return date is after request date."""
        for record in self:
            if record.expected_return_date and record.date:
                if record.expected_return_date < record.date:
                    raise ValidationError(_('Expected return date must be after request date.'))

    @api.constrains('out_date', 'returned_date')
    def _check_returned_date(self):
        """Validate that returned date is after gate out date."""
        for record in self:
            if record.out_date and record.returned_date:
                if record.returned_date < record.out_date:
                    raise ValidationError(_('Returned date must be after gate out date.'))

    @api.depends('material_lines')
    def _compute_total_items(self):
        for record in self:
            record.total_items = len(record.material_lines)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('gate.material.pass') or _('New')
        return super(MaterialPass, self).create(vals)

    def action_approve(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Only draft gate passes can be approved.'))
            if not record.material_lines:
                raise ValidationError(_('Please add at least one material item before approval.'))
            record.write({
                'state': 'approved',
                'approved_by': self.env.user.id,
                'approved_date': fields.Datetime.now(),
            })
            record.message_post(
                body=_('Gate Pass Approved\n\nApproved by: %s\nDate: %s') % (
                    self.env.user.name, 
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Gate Pass Approved')
            )

    def action_mark_out(self):
        for record in self:
            if record.state != 'approved':
                raise UserError(_('Only approved gate passes can be marked as out.'))
            record.write({
                'state': 'out',
                'out_date': fields.Datetime.now(),
                'gate_officer_id': self.env.user.id,
            })
            record.message_post(
                body=_('Material Marked as Gate Out\n\nProcessed by: %s\nDate: %s') % (
                    self.env.user.name,
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Material Gate Out')
            )

    def action_mark_returned(self):
        for record in self:
            if record.state != 'out':
                raise UserError(_('Only gate out materials can be marked as returned.'))
            record.write({
                'state': 'returned',
                'returned_date': fields.Datetime.now(),
                'gate_officer_id': self.env.user.id,
            })
            record.message_post(
                body=_('Material Marked as Returned\n\nProcessed by: %s\nReturn Date: %s') % (
                    self.env.user.name,
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Material Returned')
            )

    def action_cancel(self):
        for record in self:
            if record.state in ('returned', 'cancelled'):
                raise UserError(_('Cannot cancel a returned or already cancelled gate pass.'))
            record.write({
                'state': 'cancelled',
            })
            record.message_post(
                body=_('Gate Pass Cancelled\n\nCancelled by: %s\nDate: %s') % (
                    self.env.user.name,
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Gate Pass Cancelled')
            )

    def action_draft(self):
        for record in self:
            if record.state != 'cancelled':
                raise UserError(_('Only cancelled gate passes can be reset to draft.'))
            record.write({
                'state': 'draft',
                'approved_by': False,
                'approved_date': False,
                'out_date': False,
                'returned_date': False,
                'gate_officer_id': False,
            })
            record.message_post(
                body=_('Gate Pass Reset to Draft\n\nReset by: %s') % self.env.user.name,
                subject=_('Gate Pass Reset')
            )

