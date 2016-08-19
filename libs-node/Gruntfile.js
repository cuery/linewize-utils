"use strict";
module.exports = function(grunt) {

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        env: {
            options: {
                //Shared Options Hash
            },
            test: {
                NODE_ENV: 'test',
            },
            dev: {
                NODE_ENV: 'development',
            },
            build: {
                NODE_ENV: 'production',
            }
        },
        jshint: {
            files: ['gruntfile.js', '*.js', 'test/**/*.js'],
            options: {
                jshintrc: '.jshintrc'
            }
        },
        mochaTest: {
            test: {
                options: {
                    reporter: 'spec'
                },
                src: ['test/**/*.js']
            }
        }
    });

    grunt.loadNpmTasks('grunt-env');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-mocha-test');

    grunt.registerTask('default', ['env:test', 'jshint', 'mochaTest']);
    grunt.registerTask('test', ['env:test', 'mochaTest']);
};
