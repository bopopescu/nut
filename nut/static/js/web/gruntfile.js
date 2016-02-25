module.exports = function(grunt) {

  var files = grunt.file.expand('app/*_app.js');
  var requirejsOptions = {};
  files.forEach(function(file) {
      var filename = file.split('/')[1];
      var suffix = '.'+filename.split('.')[1];
      var name = filename.split('.')[0];
      var build_filename = name + '_build' + suffix;
      requirejsOptions[name] = {
          options: {
              baseUrl: 'app',
              mainConfigFile: 'app/config.js',
              name: name,
              out: 'jsbuild/'+build_filename,
              optimize: 'none'
          }
      };
  });

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    requirejs: requirejsOptions,
    less: {
        clean:{
            options:{
                path:['../../css/web/']
            },
            files:{
                '../../css/web/build/guoku_front.css':'../../css/web/guoku_front.less',
                '../../css/web/build/style.css':'../../css/web/style.less',
                '../../css/web/build/site.css':'../../css/web/site.less',
                '../../css/web/build/web-seller-style.css':'../../css/web/web-seller-style.less',
            }
        }
    },
    jshint: {
      files: ['*.js', '!gruntFile.js'],
      options: {
          'curly': false,
          'eqnull':true,
          'eqeqeq':false,
          'undef' :false,
          'globals':{
              "jQuery": true
          }
      }
    },
    watch:{
        scripts:{
            files:[ '**/*.js'],
            tasks:['requirejs'],
            options:{
                spawn: false,
                debounceDelay:500
            }
        }

    }
  });
  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-less');


  // Default task(s).
  grunt.registerTask('default', ['jshint']);

};