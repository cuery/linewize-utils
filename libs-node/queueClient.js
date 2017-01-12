"use strict";
/*jshint unused:false*/
var sqs = require("./aws").SQS;
var config = require('config').config;
var MongoClient = require('mongodb').MongoClient;

function AWSQueueClient() {

}

AWSQueueClient.prototype.sendMessage = function(messageBody, queueUrl, next) {
    var message = {
        MessageBody: messageBody,
        QueueUrl: queueUrl
    };
    sqs.sendMessage(message, function(err) {
        if (err) {
            next(err);
        } else {
            next();
        }
    });
};

function LocalQueueClient() {
    var self = this;
}

LocalQueueClient.prototype.runQuery = function(next) {
    if (self.db === undefined) {
        MongoClient.connect(config.MONGODB_INSTANCE + "/" + config.MONGODB_QUEUE_DB, function(err, db) {
            if (!err) {
                self.db = db;
                next();
            } else {
                console.log(err);
            }
        });
    } else {
        next();
    }
};


LocalQueueClient.prototype.sendMessage = function(msg, queue, next) {
    self.runQuery(function(msg, queue, next) {
        self.db.collection(queue).insert({
            'inProg': false,
            'done': false,
            'msg': new Buffer(msg).toString('base64')
        }, function(err){
            if (!err) {
                next();
            } else {
                console.log(err);
            }
        });
    });
};

function QueueClient(provider) {
    if (provider === "AWS") {
        return new AWSQueueClient();
    } else if (provider === "LOCAL") {
        return new LocalQueueClient();
    }
}

module.exports = QueueClient;
