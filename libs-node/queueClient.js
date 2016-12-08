"use strict";
var sqs = require("./aws").SQS;

function AWSQueueClient() {

}

AWSQueueClient.prototype.sendMessage = function (messageBody, queueUrl, next) {
    var message = {
        MessageBody: messageBody,
        QueueUrl: queueUrl
    };
    sqs.sendMessage(message, function(err){
        if (err) {
            next(err);
        } else {
            next();
        }
    });
};


function QueueClient(provider) {
    if (provider === "AWS") {
        return new AWSQueueClient();
    }
}

module.exports = QueueClient;
