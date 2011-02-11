var mustache = require('mustache');
var fs = require('fs');

var mustache_view = {
    compile: function (template, options) {
        if (typeof template == 'string') {
            return function(options) {
                options.locals = options.locals || {};
                options.partials = options.partials || {};
                if (options.body) // for express.js > v1.0
                    locals.body = options.body;
                return mustache.to_html(
                    template,
                    options.locals,
                    options.partials
                );
            };
        } else {
            return template;
        }
    },
    render: function (template, options) {
        template = this.compile(template, options);
        return template(options);
    }
};

module.exports = mustache_view;
