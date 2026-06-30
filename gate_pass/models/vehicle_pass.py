# -*- coding: utf-8 -*-

import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class VehiclePass(models.Model):
    _name = 'gate.vehicle.pass'
    _description = 'Vehicle Gate Pass'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'check_in desc, id desc'

    name = fields.Char(string='Vehicle Pass Number', required=True, readonly=True, copy=False, default=lambda self: _('New'), index=True)
    vehicle_no = fields.Char(string='Vehicle Registration Number', required=True, tracking=True, index=True)
    vehicle_type = fields.Selection([
        ('truck', 'Truck'),
        ('pickup', 'Pickup Truck'),
        ('loader', 'Loader/Excavator'),
        ('van', 'Van'),
        ('car', 'Car/Sedan'),
        ('suv', 'SUV'),
        ('motorcycle', 'Motorcycle'),
        ('bicycle', 'Bicycle'),
        ('bus', 'Bus'),
        ('trailer', 'Trailer'),
        ('other', 'Other')
    ], string='Vehicle Type', required=True, default='car', tracking=True)
    vehicle_make = fields.Char(string='Vehicle Make', tracking=True, help='e.g., Toyota, Honda, Ford')
    vehicle_model = fields.Char(string='Vehicle Model', tracking=True, help='e.g., Corolla, Civic')
    vehicle_color = fields.Char(string='Vehicle Color', tracking=True)
    driver_name = fields.Char(string='Driver Full Name', required=True, tracking=True, index=True)
    driver_license = fields.Char(string='Driver License Number', tracking=True, index=True)
    driver_phone = fields.Char(string='Driver Contact Number', required=True, tracking=True)
    driver_email = fields.Char(string='Driver Email', tracking=True)
    driver_company = fields.Char(string='Driver Company/Organization', tracking=True)
    material_description = fields.Text(string='Material/Cargo Description', tracking=True)
    purpose = fields.Text(string='Purpose of Visit', tracking=True)
    visit_type = fields.Selection([
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
        ('service', 'Service/Maintenance'),
        ('employee', 'Employee Vehicle'),
        ('visitor', 'Visitor Vehicle'),
        ('contractor', 'Contractor Vehicle'),
        ('other', 'Other')
    ], string='Visit Type', default='delivery', tracking=True)
    check_in = fields.Datetime(string='Check-In Time', required=True, default=fields.Datetime.now, tracking=True, index=True)
    check_out = fields.Datetime(string='Check-Out Time', tracking=True, index=True)
    expected_duration = fields.Float(string='Expected Duration (Hours)', tracking=True)
    gate_officer_id = fields.Many2one('res.users', string='Gate Officer', tracking=True,
                                     help='Officer who processed the vehicle entry')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, required=True, index=True)
    notes = fields.Text(string='Internal Notes', help='Internal notes visible only to authorized personnel')
    state = fields.Selection([
        ('in', 'Checked In'),
        ('out', 'Checked Out')
    ], string='Status', default='in', required=True, tracking=True)
    
    duration = fields.Float(string='Duration (Hours)', compute='_compute_duration', store=False, digits=(16, 2))

    @api.constrains('driver_email')
    def _check_email(self):
        """Validate email address format."""
        for record in self:
            if record.driver_email:
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_pattern, record.driver_email):
                    raise ValidationError(_('Please enter a valid email address for the driver.'))

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
            vals['name'] = self.env['ir.sequence'].next_by_code('gate.vehicle.pass') or _('New')
        if 'state' not in vals:
            vals['state'] = 'in'
        return super(VehiclePass, self).create(vals)

    def action_check_in(self):
        for record in self:
            if record.state != 'out':
                raise UserError(_('Vehicle is already checked in.'))
            record.write({
                'state': 'in',
                'check_in': fields.Datetime.now(),
                'check_out': False,
                'gate_officer_id': self.env.user.id,
            })
            record.message_post(
                body=_('Vehicle Checked In\n\nProcessed by: %s\nCheck-In Time: %s') % (
                    self.env.user.name,
                    fields.Datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ),
                subject=_('Vehicle Checked In')
            )

    def action_check_out(self):
        for record in self:
            if record.state != 'in':
                raise UserError(_('Vehicle must be checked in first.'))
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
                body=_('Vehicle Checked Out\n\nProcessed by: %s\nCheck-Out Time: %s\nDuration: %s hours') % (
                    self.env.user.name,
                    check_out_time.strftime('%Y-%m-%d %H:%M:%S'),
                    duration_hours
                ),
                subject=_('Vehicle Checked Out')
            )

