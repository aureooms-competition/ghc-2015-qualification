require("babel/register")({
  // This will override `node_modules` ignoring - you can alternatively pass
  // a regex
 ignore: false,
 stage: 0
});

require("./src/main.js");
