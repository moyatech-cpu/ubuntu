odoo.define('facility.fleet.dashboard', function (require) {
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

var FleetDashboardView = Widget.extend(ControlPanelMixin, {
	
//	template: 'facility.tickets_dashboard',
	events: _.extend({}, Widget.prototype.events, {
		'click #approved_bookings': 'action_approved_bookings',
		'click #rejected_bookings': 'action_rejected_bookings',
		'click #rescheduled_bookings': 'action_rescheduled_bookings',
		'click #history_bookings': 'action_history_bookings',
		'click #approved_bookings': 'action_approved_bookings',
		'click #new_booking': 'action_new_bookings',
        'click .fleet_button': 'action_fleet_button',
        'click .booked_fleet_link': 'action_booked_fleet_link',
        'click .approved_fleet_link': 'action_approved_fleet_link',
        'click .rejected_fleet_link': 'action_rejected_fleet_link',
        'click .single_record': 'action_single_record',
	}),

	init: function(parent, context) {
        this._super(parent, context);
        var fleet_data = [];
        var self = this;
        if (context.tag == 'facility.fleet_dashboard') {
            self._rpc({
                model: 'fleet.dashboard',
                method: 'get_booking_data',
            }, []).then(function(result){
                self.fleet_data = result
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
        var final_meeting_rooms_dashboard = QWeb.render( 'facility.fleet_dashboard', {
            widget: self,
        });
        $( ".o_control_panel" ).addClass( "o_hidden" );
        $(final_meeting_rooms_dashboard).prependTo(self.$el);
        return final_meeting_rooms_dashboard
    },
    reload: function () {
            window.location.href = this.href;
    },

    action_new_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("New Booking"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_rejected_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Rejected Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_state': 'rejected'
                    },
            domain: [['state', '=', 'rejected']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_rescheduled_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Rescheduled Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_rescheduled_vehicle': true
                    },
            domain: [['rescheduled_vehicle', '=', true]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_history_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("History Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_type': 'history'
                    },
            domain: [['type', '=', 'history']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_approved_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Approved Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_state': 'approved'
                    },
            domain: [['state', '=', 'approved']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_fleet_button: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_vehicle_id': parseInt(event.currentTarget.id)
                    },
            domain: [['vehicle_id', '=', parseInt(event.currentTarget.id)]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_booked_fleet_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_vehicle_id': parseInt(event.currentTarget.id),
                    'default_state': 'booked'
                    },
            domain: [['vehicle_id', '=', parseInt(event.currentTarget.id)], ['state', '=', 'booked']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_approved_fleet_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_vehicle_id': parseInt(event.currentTarget.id),
                    'default_state': 'approved'
                    },
            domain: [['vehicle_id', '=', parseInt(event.currentTarget.id)], ['state', '=', 'approved']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },
    
    action_rejected_fleet_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_vehicle_id': parseInt(event.currentTarget.id),
                    'default_state': 'rejected'
                    },
            domain: [['vehicle_id', '=', parseInt(event.currentTarget.id)], ['state', '=', 'rejected']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_single_record: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Fleet"),
            type: 'ir.actions.act_window',
            res_model: 'fleet.booking',
            view_mode: 'form',
            view_type: 'form',
            res_id: parseInt(event.currentTarget.id),
            view_id: event.currentTarget.id,
            views: [[false, 'form']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

});
core.action_registry.add('facility.fleet_dashboard', FleetDashboardView);
return FleetDashboardView
});