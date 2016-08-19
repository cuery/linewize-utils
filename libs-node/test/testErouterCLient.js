/*jshint expr: true*/
/*jshint unused: false*/

"use strict";
var assert = require('chai').assert;
var should = require('chai').should();
var erouterClient = require('../erouterClient');
var request = require('request');

describe('ERouter client', function() {
    var retyr_count = 0;
    var retries;
    var config = {};
    request.put = function(config, next){
        var err = 'Look! We found an error!';
        retyr_count++;
        if (retyr_count < retries) {
            next(err);
        } else {
            next();
        }
    };

    beforeEach(function() {
        retyr_count = 0;
    });

    it('should publish happily without error.', function(done) {
        retries = -1;
        erouterClient.publish("", "", function(err){
            assert.notOk(err);
            assert.equal(1, retyr_count);
            done();
        });
    });

    it('should retry publish in case of error.', function(done) {
        retries = 2;
        erouterClient.publish("", "", function(err){
            assert.notOk(err);
            assert.equal(2, retyr_count);
            done();
        });
    });

    it('should throw exception if publish retry does not work.', function(done) {
        retries = 12;
        erouterClient.publish("", "", function(err){
            assert.ok(err);
            assert.equal(11, retyr_count);
            done();
        });
    });
});
