// this is for older browser support
var inHeadTS=(new Date()).getTime();

// plugin
function s_getLoadTime(){if(!window.s_loadT){var b=new Date().getTime(),o=window.performance?performance.timing:0,a=o?o.requestStart:window.inHeadTS||0;s_loadT=a?Math.round((b-a)/100):''}return s_loadT}

// call plugin first time 
s_getLoadTime();
