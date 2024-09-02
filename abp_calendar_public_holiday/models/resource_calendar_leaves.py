# -- coding: utf-8 --

from odoo import models, fields, api


class ResourceCalendarLeaves(models.Model):   
    _inherit = 'resource.calendar.leaves'
    
    abp_allday = fields.Boolean(string='All Day', default=True)
    abp_calendar_event = fields.Many2one('calendar.event', string='Calendar Event')

    @api.model_create_multi
    def create(self, vals_list):
        leaves = super(ResourceCalendarLeaves, self).create(vals_list)
        
        for leave in leaves:
            if not leave.holiday_id or not leave.holiday_id.id:
                partners = self.env['res.users'].search([('share','=',False)]).partner_id.mapped('id')           
                event = self.env['calendar.event'].create({
                    'name': 'Day off - ' + leave.name,
                    'partner_ids': partners,
                    'start': leave.date_from,
                    'stop': leave.date_to,
                    'abp_resource_calendar_leaves': leave.id,
                    'allday' : leave.abp_allday,
                })
                leave.abp_calendar_event = event
    
        return leaves
    
    def write(self, vals):
        # OVERRIDE
        leave = super(ResourceCalendarLeaves, self).write(vals)
        if not self.holiday_id or not self.holiday_id.id:
            event = self.abp_calendar_event
            if event:
                val_to_update = {}
                if 'name' in vals:
                    val_to_update['name'] = 'Day off - ' + self.name
                if 'date_from' in vals:
                    val_to_update['start'] = self.date_from
                if 'date_to' in vals:
                    val_to_update['stop'] = self.date_to
                if 'abp_allday' in vals:
                    val_to_update['allday'] = self.abp_allday
                if val_to_update:
                    event.write(val_to_update)
        return leave
    
    
    
    
    
    