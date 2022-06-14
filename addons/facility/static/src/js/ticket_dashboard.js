odoo.define('facility.dashboard', function (require) {
"use strict";

var core = require('web.core');
var session = require('web.session');
var ajax = require('web.ajax');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var Widget = require('web.Widget');
var ControlPanelMixin = require('web.ControlPanelMixin');
var rpc = require('web.rpc');

var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;

var TicketDashboardView = Widget.extend(ControlPanelMixin, {
//	template: 'facility.tickets_dashboard',
	events: _.extend({}, Widget.prototype.events, {
		'click #my_tickets_view': 'action_my_tickets_view',
		'click #my_tickets_normal_view': 'action_my_tickets_normal_view',
		'click #my_tickets_hp_view': 'action_my_tickets_hp_view',
		'click #my_tickets_urgent_view': 'action_my_tickets_urgent_view',
		'click #my_sla_failed_tickets_view': 'action_my_sla_failed_tickets_view',
        'click #my_sla_failed_normal_tickets_view': 'action_my_sla_failed_normal_tickets_view',
		'click #my_sla_failed_high_tickets_view': 'action_my_sla_failed_high_tickets_view',
		'click #my_sla_failed_urgent_tickets_view': 'action_my_sla_failed_urgent_tickets_view',
        'click .tickets_view': 'action_tickets_view',
        'click .category_button': 'action_category_tickets_view',
        'click .category_unassigned_link': 'action_category_unassigned_link',
        'click .category_high_priority_link': 'action_category_high_priority_link',
        'click .category_urgent_link': 'action_category_urgent_link',
//        'click #generate_payroll_pdf': function(){this.generate_payroll_pdf("bar");},
//        'click #generate_attendance_pdf': function(){this.generate_payroll_pdf("pie")},
//        'click .my_profile': 'action_my_profile',
	}),

	init: function(parent, context) {
        this._super(parent, context);
        var tickets_data = [];
        var self = this;
        self.next_action = true

        this.getSession().user_has_group('facility.facility_officer').then(function(has_group) {
            if(has_group) {
                self.next_manager = false;
            }
        })



      /*  this.getSession().user_has_group('facility.facility.end_user').then(function(has_group) {
            if(has_group) {
                self.next_action = true;
            }
        })*/

//        console.log(self.next_action,"-----");
//        self.next_action = false;
        if (context.tag == 'facility.tickets_dashboard') {
            self._rpc({
                model: 'ticket.dashboard',
                method: 'get_data',
            }, []).then(function(result){
                self.tickets_data = result
                console.log(self.tickets_data);
            }).done(function(){
                self.render();
                self.href = window.location.href;
            });
        }
    },
    willStart: function() {
         return $.when(ajax.loadLibs(this), this._super());
    },
    start: function() {
        var self = this;
        return this._super();
    },
    render: function() {
        var super_render = this._super;
        var self = this;
        var helpdesk_ticket_dashboard = '';
        
        this.getSession().user_has_group('facility.facility_manager').then(function(has_group) {
            if(has_group) {
                helpdesk_ticket_dashboard = QWeb.render( 'facility.tickets_dashboard_officer', {
                    widget: self,
                });
            }
        })
        
        this.getSession().user_has_group('facility.facility_officer').then(function(has_group) {
            if(has_group) {
                helpdesk_ticket_dashboard = QWeb.render( 'facility.tickets_dashboard_officer', {
                    widget: self,
                });
            }
        })
        
        this.getSession().user_has_group('facility.end_user').then(function(has_group) {
            if(has_group) {
                helpdesk_ticket_dashboard = QWeb.render( 'facility.tickets_dashboard_end_user', {
                    widget: self,
                });
            }
        })
        
        
        $( ".o_control_panel" ).addClass( "o_hidden" );
        $(helpdesk_ticket_dashboard).prependTo(self.$el);
        return helpdesk_ticket_dashboard
    },
    reload: function () {
            window.location.href = this.href;
    },

    action_my_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {
                    'default_user_id': self.tickets_data.uid
                    },
            domain: [['user_id', '=', self.tickets_data.uid]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_tickets_normal_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Tickets(Normal Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_user_id': self.tickets_data.uid,
                    'default_priority': '1'
                    },
            domain: [['user_id', '=', self.tickets_data.uid], ['priority', '=', '1']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_tickets_hp_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Tickets(High Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_user_id': self.tickets_data.uid,
                    'default_priority': '2'
                    },
            domain: [['user_id', '=', self.tickets_data.uid], ['priority', '=', '2']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_tickets_urgent_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My Tickets(Urgent Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_user_id': self.tickets_data.uid,
                    'default_priority': '3'
                    },
            domain: [['user_id', '=', self.tickets_data.uid], ['priority', '=', '3']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_sla_failed_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My SLA Failed Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['user_id', '=', self.tickets_data.uid], ['is_mailed_sla', '=', true]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_sla_failed_normal_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My SLA Failed Tickets(Normal Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['user_id', '=', self.tickets_data.uid], ['is_mailed_sla', '=', true], ['priority', '=', '1']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_sla_failed_high_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My SLA Failed Tickets(High Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['user_id', '=', self.tickets_data.uid], ['is_mailed_sla', '=', true], ['priority', '=', '2']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_my_sla_failed_urgent_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("My SLA Failed Tickets(Urgent Priority)"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            domain: [['user_id', '=', self.tickets_data.uid], ['is_mailed_sla', '=', true], ['priority', '=', '3']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'kanban,tree,form',
            view_type: 'form',
            views: [[false, 'kanban'],[false, 'list'],[false, 'form']],
            context: {
                    'default_stage_id': parseInt(event.currentTarget.id)
                    },
            domain: [['stage_id', '=', parseInt(event.currentTarget.id)]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_category_tickets_view: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_helpdesk_category_id': parseInt(event.currentTarget.id)
                    },
            domain: [['helpdesk_category_id', '=', parseInt(event.currentTarget.id)]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_category_unassigned_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_helpdesk_category_id': parseInt(event.currentTarget.id),
                    'default_user_id': false
                    },
            domain: [['helpdesk_category_id', '=', parseInt(event.currentTarget.id)], ['user_id', '=', false]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_category_high_priority_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_helpdesk_category_id': parseInt(event.currentTarget.id),
                    'default_priority': '2'
                    },
            domain: [['helpdesk_category_id', '=', parseInt(event.currentTarget.id)], ['priority', '=', '2']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_category_urgent_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'helpdesk_lite.ticket',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_helpdesk_category_id': parseInt(event.currentTarget.id),
                    'default_priority': '3'
                    },
            domain: [['helpdesk_category_id', '=', parseInt(event.currentTarget.id)], ['priority', '=', '3']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
});
core.action_registry.add('facility.tickets_dashboard', TicketDashboardView);
return TicketDashboardView
});