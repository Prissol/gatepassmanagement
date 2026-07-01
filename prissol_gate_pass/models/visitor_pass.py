# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class VisitorPass(models.Model):
    _name = 'gate.visitor.pass'
    _description = 'Visitor Gate Pass'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'check_in desc, id desc'

    name = fields.Char(string='Visitor Pass Number', required=True, readonly=True, copy=False, default=lambda self: _('New'), index=True)
    visitor_name = fields.Char(string='Visitor Full Name', required=True, tracking=True, index=True)
    visitor_first_name = fields.Char(string='First Name', tracking=True)
    visitor_last_name = fields.Char(string='Last Name', tracking=True)
    visitor_email = fields.Char(string='Email Address', tracking=True)
    visitor_phone = fields.Char(string='Phone Number', tracking=True, index=True)
    visitor_mobile = fields.Char(string='Mobile Number', tracking=True)
    id_type = fields.Selection([
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
        ('company_id', 'Company ID'),
        ('other', 'Other')
    ], string='ID Type', default='national_id', tracking=True)
    visitor_id_number = fields.Char(string='ID Number', tracking=True, index=True, 
                                   help='National ID, Passport Number, or other identification number')
    visitor_cnic = fields.Char(string='CNIC/NICOP', tracking=True, 
                             help='National Identity Card Number (for backward compatibility)')
    company_name = fields.Char(string='Company/Organization', tracking=True, index=True)
    company_address = fields.Text(string='Company Address', tracking=True)
    person_to_meet = fields.Many2one('hr.employee', string='Person to Meet', required=True, tracking=True, index=True)
    department_to_visit = fields.Many2one('hr.department', string='Department to Visit', tracking=True)
    check_in = fields.Datetime(string='Check-In Time', required=False, tracking=True, index=True)
    check_out = fields.Datetime(string='Check-Out Time', tracking=True, index=True)
    expected_duration = fields.Float(string='Expected Duration (Hours)', tracking=True, 
                                     help='Expected duration of visit in hours')
    purpose = fields.Text(string='Purpose of Visit', required=True, tracking=True)
    visit_type = fields.Selection([
        ('business', 'Business Meeting'),
        ('interview', 'Job Interview'),
        ('delivery', 'Delivery/Pickup'),
        ('maintenance', 'Maintenance/Service'),
        ('inspection', 'Inspection/Audit'),
        ('training', 'Training'),
        ('other', 'Other')
    ], string='Visit Type', default='business', tracking=True)
    card_no = fields.Char(string='Visitor Badge Number', tracking=True, index=True)
    vehicle_brought = fields.Boolean(string='Vehicle Brought', default=False, tracking=True)
    vehicle_number = fields.Char(string='Vehicle Registration', tracking=True)
    gate_officer_id = fields.Many2one('res.users', string='Gate Officer', tracking=True,
                                     help='Officer who processed the visitor entry')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True, index=True)
    notes = fields.Text(string='Internal Notes', help='Internal notes visible only to authorized personnel')
    state = fields.Selection([
        ('in', 'Checked In'),
        ('out', 'Checked Out')
    ], string='Status', default='out', required=True, tracking=True)
    
    duration = fields.Float(string='Duration (Hours)', compute='_compute_duration', store=False, digits=(16, 2))

    @api.constrains('visitor_email')
    def _check_email(self):
        """Validate email address format."""
        for record in self:
            if record.visitor_email:
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, record.visitor_email):
                    raise ValidationError(_('Please enter a valid email address for the visitor.'))

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        """Validate that check-out time is after check-in time."""
        for record in self:
            if record.check_in and record.check_out:
                if record.check_out < record.check_in:
                    raise ValidationError(_('Check-out time must be after check-in time.'))

    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.duration = round(delta.total_seconds() / 3600.0, 2)
            elif record.check_in:
                # Calculate current duration if still checked in
                delta = fields.Datetime.now() - record.check_in
                record.duration = round(delta.total_seconds() / 3600.0, 2)
            else:
                record.duration = 0.0

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('gate.visitor.pass') or _('New')
        if 'state' not in vals:
            vals['state'] = 'out'
        return super(VisitorPass, self).create(vals)

    def action_check_in(self):
        for record in self:
            if record.state != 'out':
                raise UserError(_('Visitor is already checked in.'))
            if not record.visitor_name:
                raise ValidationError(_('Please enter visitor name before checking in.'))
            record.write({
                'state': 'in',
                'check_in': fields.Datetime.now(),
                'check_out': False,
                'gate_officer_id': self.env.user.id,
            })
            record.message_post(
                body=_('Visitor Checked In\n\nProcessed by: %s\nCheck-In Time: %s') % (
                    self.env.user.name,
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Visitor Checked In')
            )

    def action_check_out(self):
        for record in self:
            if record.state != 'in':
                raise UserError(_('Visitor must be checked in first.'))
            check_out_time = fields.Datetime.now()
            duration_hours = 0.0
            if record.check_in:
                delta = check_out_time - record.check_in
                duration_hours = round(delta.total_seconds() / 3600.0, 2)
            record.write({
                'state': 'out',
                'check_out': check_out_time,
                'gate_officer_id': self.env.user.id,
            })
            record.message_post(
                body=_('Visitor Checked Out\n\nProcessed by: %s\nCheck-Out Time: %s\nDuration: %s hours') % (
                    self.env.user.name,
                    check_out_time.strftime('%Y-%m-%d %H:%M:%S'),
                    duration_hours
                ),
                subject=_('Visitor Checked Out')
            )

