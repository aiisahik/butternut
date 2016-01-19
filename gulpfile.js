var gulp = require('gulp'),
    assets = require('./gulpassets.js'),
    sass = require('gulp-sass'),
    // autoprefix = require('gulp-autoprefixer'),
    ngHtml2Js = require('gulp-ng-html2Js'),
    concat = require('gulp-concat'),
    install = require("gulp-install"),
    gutil = require("gulp-util"),
    runSequence = require('run-sequence'),
    mainBowerFiles = require('main-bower-files'),
    inject = require('gulp-inject'),
    _ = require('lodash'),
    minifyCSS = require('gulp-minify-css'),
    sourcemaps = require('gulp-sourcemaps'),
    clean = require('gulp-clean'),
    rename = require("gulp-rename"),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant'),
    uglify = require('gulp-uglify');

// assets.init(gutil.env.type || 'local');

var staticRoot = 'butternut/static/';

// ===  task definitions === //

//this task compiles sass to css and handles browser specific css tags for the previous two versions
gulp.task('sass', function () {
    return gulp.src(assets.sass)
        .pipe(sass({
            errLogToConsole: true
        }).on('error', gutil.log))
        // .pipe(autoprefix('last 2 version'))
        .pipe(gulp.dest(assets.destinations.css));
});
gulp.task('concat-css-public', function () {
    return gulp.src(assets.pathify(assets.cssPublic))
        .pipe(concat("public.min.css")
            .on('error', gutil.log))
        .pipe(gulp.dest(assets.destinations.css)
            .on('error', gutil.log));
});

//concatinate js files for each app
gulp.task('concat-js-public', function () {
    return gulp.src(assets.pathify(assets.jsPublic))
        .pipe(uglify().on('error', gutil.log))
        .pipe(concat("public.min.js"))
        .pipe(gulp.dest(assets.destinations.js));
});


// === template task definitions === //
// concatinate the angular html templates into a js file for client side caching for each app
gulp.task('html2js-public', function () {
    return gulp.src(assets.templatesPublic)
        .pipe(ngHtml2Js({
            moduleName: "butternut.public.templates",
            rename: function (url) {
                return assets.destinations.getTemplatesPublicUrl(url);
            }
        }))
        .pipe(concat(assets.destinations.templatesPublicJS))
        .pipe(gulp.dest(assets.destinations.templatesPublicDir));
});

// end concatinate the angular html templates
gulp.task('images', function() {
    return gulp.src(assets.images)
        .pipe(imagemin({
            progressive: true,
            svgoPlugins: [{removeViewBox: false}],
            use: [pngquant()]
        }))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(assets.destinations.images));
});

// clear out destination directories
gulp.task('clean', function () {
    return gulp.src([
        assets.destinations.css,
        assets.destinations.js,
        assets.destinations.templatesPublicDir
    ], {read: false}).pipe(clean())
});
// end clear out destination directories

// install files in bower.json and package.json
gulp.task('install', function () {
    return gulp.src(['./bower.json', './package.json'])
        .pipe(install());
});


// get a list of the main js files from bower and copy them to libs folder
gulp.task('bower', function () {
    return gulp.src(mainBowerFiles(), {
        // base: staticRoot + 'bower_components'
        base: 'bower_components'
    })
    .pipe(gulp.dest(staticRoot + 'libs'));
});


// this task injects the css and js filepaths into cssHeader, jsFooter etc.
// see documentation for gulp-inject

gulp.task('index', function () {
    _.forEach(assets.injections, function (inj) {
        gulp.src(inj.srcFile)
            .pipe(inject(gulp.src(inj.files1, {read: false})
                , {
                    name: inj.name1, transform: function (filepath) {
                        if (inj.type == 'js') {
                            return assets.generateStaticJSPath(filepath);
                        }
                        else if (inj.type == 'css') {
                            return assets.generateStaticCSSPath(filepath);
                        }
                    }
                }))
                .pipe(inject(gulp.src(inj.files2, {read: false})
                , {
                    name: inj.name2, transform: function (filepath) {
                        if (inj.type == 'js') {
                            return assets.generateStaticJSPath(filepath);
                        }
                        else if (inj.type == 'css') {
                            return assets.generateStaticCSSPath(filepath);
                        }
                    }
                }))
            .pipe(gulp.dest(inj.destFolder));
    })
});

// cleans out the libs directory. Probably don't need to ever call this
gulp.task('bower-clean', function () {
    return gulp.src([staticRoot + 'libs'], {read: false}).pipe(clean());
});

// start a watcher for sass changes - this will autocompile to css
gulp.task('watch-sass', function () {
   return gulp.watch(staticRoot + 'css/src/**/**/*.scss', ['sass']);
});

// watch for bower changes
gulp.task('watch-bower', function () {
    return gulp.watch(staticRoot + 'bower_components/**', ['bower']);
});

// sequence of tasks that run when you run the gulp command
gulp.task('default', function(callback){
    runSequence('install','sass', ['watch-sass']);
});
//gulp.task('build', ['clean', 'html2js', 'sass', 'concat-css', 'concat-js', 'index']);

// sequence of tasks that run when you run the gulp build command.
gulp.task('build', function (callback) {
    runSequence('install', 'clean', 'sass', 'html2js-public','concat-css-public','concat-js-public', 'index');
});
