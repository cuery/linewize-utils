"use strict";
var request = require('request');
var uuid = require('node-uuid');

var service_url;
var publish_retry_count = 10;

var poll = function(topic_name, subscription_name, next) {
    request.get(service_url + "/topic/" + topic_name + "/" + subscription_name + "/poll", function(err, response, body) {
        if (err) {
            setTimeout(function() {
                poll(topic_name, subscription_name, next);
            }, 100);
            next(err);
        } else {
            try {
                var json_blob = JSON.parse(body);
                if (json_blob.message) {
                    var msg = JSON.parse(json_blob.message);
                    request.del(service_url + "/topic/" + topic_name + "/" + subscription_name + "/delete/" + msg['id'], function(err) {
                        if (err) {
                            next(err);
                        } else {
                            next(null, msg['msg']);
                        }
                        poll(topic_name, subscription_name, next);
                    });
                } else {
                    setTimeout(function() {
                        poll(topic_name, subscription_name, next);
                    }, 1000);
                }
            } catch (err) {
                setTimeout(function() {
                    poll(topic_name, subscription_name, next);
                }, 100);
                next(err);
            }
        }
    });
};

var subscribe = function(topic_name, subscription_name, next) {
    subscription_name  += '_' + uuid.v4();
    request.post(service_url + "/topic/" + topic_name + "/" + subscription_name + "/subscribe", function(err) {
        if (err) {
            next(err);
        } else {
            poll(topic_name, subscription_name, next);
        }
    });
};

var publish = function(topic_name, message, next, retries) {
    retries = typeof retries !== 'undefined' ? retries : 0;
    request.put({
        headers: {
            'content-type': 'application/json'
        },
        url: service_url + '/topic/' + topic_name + '/publish',
        body: message
    }, function(err) {
        if (err) {
            if (retries < publish_retry_count) {
                retries++;
                setTimeout(function() {
                    publish(topic_name, message, next, retries);
                }, 100);
            } else {
                next(err);
            }
        } else {
            next();
        }
    });
};

exports.subscribe = subscribe;
exports.publish = publish;
exports.set_service_url = function(url) {
    service_url = url;
};
