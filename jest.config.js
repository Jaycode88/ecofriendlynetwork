module.exports = {
    testEnvironment: 'jsdom',
    moduleDirectories: [
      "node_modules",
      // path to  JavaScript files 
      "<ecofriendlynetwork>/static/js"
    ],
    transform: {
      // Transform files with a .js or .jsx extension using babel-jest
      "^.+\\.jsx?$": "babel-jest"
    },
  };
  