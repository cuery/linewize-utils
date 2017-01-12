"use strict";
var path = require('path');
var s3 = require("./aws").S3;
var fs = require('fs');

function AWSFileClient() {

}

AWSFileClient.prototype.putFile = function(fileName, fileBody, folder, next) {
    var data = {
        Key: fileName,
        Body: fileBody,
        Bucket: folder
    };
    s3.putObject(data, function(err) {
        if (err) {
            next(err);
        } else {
            next();
        }
    });
};

function LocalFileClient() {

}

LocalFileClient.prototype.putFile = function(fileName, fileBody, folder, next) {
    fs.writeFile(path.join(folder, fileName), fileBody, function(err) {
        if (err) {
            next(err);
        } else {
            next();
        }
    });
};

function FileClient(provider) {
    if (provider === "AWS") {
        return new AWSFileClient();
    } else if (provider === "LOCAL") {
        return new LocalFileClient();
    }
}

module.exports = FileClient;
