'use strict';
function candies(kids) {
    var sum = 0;
    sum += kids.forEach(function (kid) {
        return kid;
    });
    return sum / kids.length;
}