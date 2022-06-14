odoo.define('facility.meeting.room.dashboard', function (require) {
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

var MeetingRoomsDashboardView = Widget.extend(ControlPanelMixin, {
//	template: 'facility.tickets_dashboard',
	events: _.extend({}, Widget.prototype.events, {
		'click #cancelled_bookings': 'action_cancelled_bookings',
		'click #rescheduled_bookings': 'action_rescheduled_bookings',
		'click #history_bookings': 'action_history_bookings',
		'click #confirmed_bookings': 'action_confirmed_bookings',
		'click #new_booking': 'action_new_bookings',
        'click .room_button': 'action_room_button',
        'click .booked_room_link': 'action_booked_room_link',
        'click .cancelled_room_link': 'action_cancelled_room_link',
        'click .single_record': 'action_single_record',
	}),

	init: function(parent, context) {
        this._super(parent, context);
        var meeting_data = [];
        var self = this;
        if (context.tag == 'facility.meeting_rooms_dashboard') {
            self._rpc({
                model: 'meeting.dashboard',
                method: 'get_booking_data',
            }, []).then(function(result){
                self.meeting_data = result
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
        var final_meeting_rooms_dashboard = QWeb.render( 'facility.meeting_rooms_dashboard', {
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
            res_model: 'meeting.room.booking',
            view_mode: 'form',
            view_type: 'form',
            views: [[false, 'form']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_cancelled_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Cancelled Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_state': 'cancelled'
                    },
            domain: [['state', '=', 'cancelled']],
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
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_rescheduled_room': true
                    },
            domain: [['rescheduled_room', '=', true]],
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
            res_model: 'meeting.room.booking',
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

    action_confirmed_bookings: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Confirmed Bookings"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_state': 'booked'
                    },
            domain: [['state', '=', 'booked']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_room_button: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_meeting_room_id': parseInt(event.currentTarget.id)
                    },
            domain: [['meeting_room_id', '=', parseInt(event.currentTarget.id)]],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_booked_room_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_meeting_room_id': parseInt(event.currentTarget.id),
                    'default_state': 'booked'
                    },
            domain: [['meeting_room_id', '=', parseInt(event.currentTarget.id)], ['state', '=', 'booked']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_cancelled_room_link: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Tickets"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'tree,form',
            view_type: 'form',
            views: [[false, 'list'],[false, 'form']],
            context: {
                    'default_meeting_room_id': parseInt(event.currentTarget.id),
                    'default_state': 'cancelled'
                    },
            domain: [['meeting_room_id', '=', parseInt(event.currentTarget.id)], ['state', '=', 'cancelled']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

    action_single_record: function(event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        this.do_action({
            name: _t("Meeting Rooms"),
            type: 'ir.actions.act_window',
            res_model: 'meeting.room.booking',
            view_mode: 'form',
            view_type: 'form',
            res_id: parseInt(event.currentTarget.id),
            view_id: event.currentTarget.id,
            views: [[false, 'form']],
            target: 'current'
        },{on_reverse_breadcrumb: function(){ return self.reload();}})
    },

});
core.action_registry.add('facility.meeting_rooms_dashboard', MeetingRoomsDashboardView);
return MeetingRoomsDashboardView
});