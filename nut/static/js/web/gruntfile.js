module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
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

    requirejs:{
        compile_selection_entity:{
            options:{
                baseUrl: 'app/',
                mainConfigFile: 'app/config.js',
                name: 'selection_entity_app',
                out: 'jsbuild/selection_entity_app_build.js',
                optimize:'none'
            }
        },
        compile_article_list:{
            options:{
                baseUrl: 'app/',
                mainConfigFile: 'app/config.js',
                name: 'article_list_app',
                out: 'jsbuild/article_list_app_build.js',
                optimize: 'none'
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

  // Default task(s).
  grunt.registerTask('default', ['jshint']);

};