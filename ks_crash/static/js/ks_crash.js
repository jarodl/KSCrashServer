$(function(){

    var Item = Backbone.Model.extend({
        set: function(attributes, options) {
            attributes['id'] = attributes['ident'];
            attributes['content'] = JSON.stringify(attributes['content'], null, 4)
            Backbone.Model.prototype.set.call(this, attributes, options);
        }
    });

    var Report = Item.extend({
    });

    var ItemView = Backbone.View.extend({
        tagName: "div",
    });

    var ReportView = ItemView.extend({
        className: "report item accordion-group",

        template: _.template($('#report').html()),

        initialize: function() {
            this.model.bind('change', this.render, this);
            this.model.bind('destroy', this.remove, this);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
    });

    var ItemList = Backbone.Collection.extend({
        model: Report,

        url: '/api/reports.json',

        comparator: function(item) {
            return item.get('ident');
        },

        parse: function(response) {
            return response.reports;
        }
    });

    var Reports = new ItemList;

    var AppView = Backbone.View.extend({
        el: $('#reports'),

        initialize: function() {
            this.jug = new Juggernaut();
            this.jug.subscribe('report-channel', this.addLatestReport);

            Reports.bind('add', this.addLatestReportToView, this);
            Reports.bind('reset', this.addLatestReports, this);

            Reports.fetch();
        },

        addLatestReports: function() {
            Reports.each(this.addLatestReportToView);
        },

        addLatestReport: function(report) {
            var item = Reports.get(report['ident']);
            if (!item) {
                item = new Report(report);
                Reports.create(item);
            }
            else {
                item.set(report);
            }
        },

        addLatestReportToView: function(item) {
            var view = new ReportView({
                model: item,
                id: "report-" + item.get('ident')
            });
            var new_item = view.render().el;
            $('#reports').append(new_item);
        }
    });

    var App = new AppView;

});
