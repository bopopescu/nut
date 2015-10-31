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
        compile:{
            options:{
                baseUrl: 'app/',
                mainConfigFile: 'app/config.js',
                name: 'selection_entity_app',
                out: 'build/selection_entity_app_build.js'
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