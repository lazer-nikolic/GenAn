var queryOps = {
    "starts_with" : function(field, param){
        retVal = {}
        retVal[field] = new RegExp("^" + param);
        return retVal;
    },
    "ends_with" : function(field, param){
        retVal = {}
        retVal[field] = new RegExp(param + "$");
        return retVal;
    },
    "contains" : function(field, param){
        retVal = {}
        retVal[field] = new RegExp(param);
        return retVal;
    },
    "gt": function(field, param){
        retVal = {}
        retVal[field] = {$gt : param};
        return retVal;
    },
    "lt": function(field, param){
        retVal = {}
        retVal[field] = {$lt : param};
        return retVal;
    },
    "gte": function(field, param){
        retVal = {}
        retVal[field] = {$gte : param};
        return retVal;
    },
    "lte": function(field, param){
        retVal = {}
        retVal[field] = {$lte : param};
        return retVal;
    },

}

module.exports = queryOps;