var _ = require('lodash');
var staticRoot = 'ittakes2/static/',
    staticPath = '/static/',
    templateRoot = 'ittakes2/templates/',
    css = staticRoot + 'css/dist',
    images = staticRoot + 'images/src/**/**/*',
    js = staticRoot + 'js/dist';

var pathify = function (arr) {
    return _.map(arr, function (v) {
        return staticRoot + v;
    })
};


// arrays of static assets grouped. These are concatenated together
var jsLibs = [
    'libs/lodash/lodash.js',
    'libs/angular/angular.js',
    'libs/angular-resource/angular-resource.js',
    'libs/angular-ui-router/release/angular-ui-router.js',
    'libs/angular-ui-bootstrap-bower/ui-bootstrap-tpls.js'
];

var jsPublic = [
    'libs/lodash/lodash.js',
    'libs/angular/angular.js',
    'libs/angular-resource/angular-resource.js',
    'libs/angular-ui-router/release/angular-ui-router.js',
    'libs/angular-ui-bootstrap-bower/ui-bootstrap-tpls.js',
    'js/app.js',
    'js/services.js',
    'js/api.js',
    'js/controllers.js'
];

var jsPublicDummyTemplates = [
    'templates/public-templates.js'
];

var jsPublicTemplates = [
    'templates/dist/public-templates.min.js'
];

var cssPublic = [
    'css/dist/public.css'
];

var templatesPublicJS = 'public-templates.min.js',
    templatesPublicDir = staticRoot + 'js/public/templates/dist';
    
// exports making these variables visible to the gulpfile.js

module.exports = {
    jsLibs: jsLibs,
    jsPublic: jsPublic,
    jsPublicDummyTemplates: jsPublicDummyTemplates,
    jsPublicTemplates: jsPublicTemplates,
    templatesPublic: staticRoot + 'templates/**/**/*.tpl.html',
    sass: staticRoot + 'css/src/**/**/*.scss',
    images: images,
    destinations: {
        images: staticRoot + 'images/dist',
        css:css,
        js: js,
        templatesPublicJS: templatesPublicJS,
        templatesPublicDir: templatesPublicDir,
        getTemplatesPublicUrl: function (file) {
            return staticPath + 'templates/' + file;
        },
    },
    pathify: function (arr) {
        return _.map(arr, function (v) {
            return staticRoot + v;
        })
    },
    generateStaticJSPath: function (filepath) {
        var subpath = filepath.split(staticRoot)[1];
        return '<script type="text/javascript" src="{% static \'' + subpath + '\' %}"></script>';
    },
    generateStaticCSSPath: function (filepath) {
        var subpath = filepath.split(staticRoot)[1];
        return '<link type="text/css" rel="stylesheet" href="{% static \'' + subpath + '\' %}"/>';
    },
    injections: [
        // info about the files that need to be injected into jsfooter/cssheader etc
        {
            module: 'public.jsFooter',
            type: 'js',
            srcFile: templateRoot + 'base/_js_footer.html',
            destFolder: templateRoot + 'base/',
            name1: 'raw',
            files1: _.union(pathify(jsPublic), pathify(jsPublicDummyTemplates)),
            name2: 'minified',
            files2: [js + '/libs.min.js', js + '/public.min.js', templatesPublicDir + '/' + templatesPublicJS ]
        },
        {
            module: 'public.cssHeader',
            type: 'css',
            srcFile: templateRoot + 'base/_css_header.html',
            destFolder: templateRoot + 'base/',
            name1: 'raw',
            files1: pathify(cssPublic),
            name2: 'minified',
            files2: [css + '/public.min.css']
        }
    ]

};