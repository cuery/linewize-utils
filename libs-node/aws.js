/*jshint loopfunc: true */
"use strict";

var config = require('config').config;
var AWS = require('aws-sdk');

var ep = new AWS.Endpoint(config.AWS_S3_ENDPOINT);
var s3 = new AWS.S3({
    endpoint: ep,
    accessKeyId: config.AWS_ACCESS_KEY_ID,
    secretAccessKey: config.AWS_SECRET_ACCESS_KEY,
    params: {
        Bucket: config.DATA_INPUT_BUCKET
    }
});
var sqs = new AWS.SQS({
    region: config.AWS_SQS_REGION,
    accessKeyId: config.AWS_ACCESS_KEY_ID,
    secretAccessKey: config.AWS_SECRET_ACCESS_KEY
});

exports.SQS = sqs;
exports.S3 = s3;
