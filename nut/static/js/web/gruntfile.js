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
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default task(s).
  grunt.registerTask('default', ['jshint']);

};