"use strict";
var s2 = require("./aws").S3;

function AWSFileClient() {

}

AWSFileClient.prototype.putFile(fileName, fileBody, folder, next) {
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


function FileClient(provider) {
    if (provider === "AWS") {
        return new AWSFileClient();
    }
}

module.exports = FileClient;
