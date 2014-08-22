module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      all: ['Gruntfile.js', 'static/js/*.js']
    },
    htmllint: {
      all: ['static/*.html']
    },
    csslint: {
      all: 'static/css/*.css'
    },
    jsonlint: {
      all: 'jsonschema/*.json',
      files: ['package.json']
    },
    flake8: {
      src: ['src/**/*.py'],
    },
    nose: {
      main: {}
    }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-html');
  grunt.loadNpmTasks('grunt-contrib-csslint');
  grunt.loadNpmTasks('grunt-jsonlint');
  grunt.loadNpmTasks('grunt-flake8');
  grunt.loadNpmTasks('grunt-nose');

  // Default task(s).
  grunt.registerTask('default', ['jshint', 'htmllint', 'jsonlint', 'flake8', 'nose', 'csslint']);

};
