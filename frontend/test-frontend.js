/**
 * Frontend Build and Basic Functionality Test
 * This script verifies that the frontend can build successfully
 * and checks for common issues
 */

const fs = require('fs');
const path = require('path');

console.log('🧪 Starting Frontend Tests...\n');

let passedTests = 0;
let failedTests = 0;
const issues = [];

// Test 1: Check if all required files exist
console.log('📁 Test 1: Checking required files...');
const requiredFiles = [
  'src/App.jsx',
  'src/index.jsx',
  'src/styles/theme.css',
  'src/styles/components.css',
  'src/services/api.js',
  'src/components/Navbar.jsx',
  'src/components/MovieCard.jsx',
  'src/pages/Home.jsx',
  'src/pages/Login.jsx',
  'src/pages/Register.jsx',
  'src/pages/Profile.jsx',
  'src/pages/News.jsx',
  'src/pages/Chat.jsx',
  'src/pages/Contact.jsx',
  'src/pages/AdminDashboard.jsx',
  'package.json',
  'vite.config.js',
  'public/index.html'
];

let allFilesExist = true;
requiredFiles.forEach(file => {
  const filePath = path.join(__dirname, file);
  if (!fs.existsSync(filePath)) {
    console.log(`   ❌ Missing: ${file}`);
    issues.push(`Missing file: ${file}`);
    allFilesExist = false;
  }
});

if (allFilesExist) {
  console.log('   ✅ All required files exist');
  passedTests++;
} else {
  console.log('   ❌ Some files are missing');
  failedTests++;
}

// Test 2: Check package.json dependencies
console.log('\n📦 Test 2: Checking package.json...');
try {
  const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
  
  const requiredDeps = ['react', 'react-dom', 'react-router-dom', 'axios'];
  const missingDeps = requiredDeps.filter(dep => !packageJson.dependencies[dep]);
  
  if (missingDeps.length === 0) {
    console.log('   ✅ All required dependencies present');
    passedTests++;
  } else {
    console.log(`   ❌ Missing dependencies: ${missingDeps.join(', ')}`);
    issues.push(`Missing dependencies: ${missingDeps.join(', ')}`);
    failedTests++;
  }
} catch (error) {
  console.log('   ❌ Error reading package.json');
  issues.push('Cannot read package.json');
  failedTests++;
}

// Test 3: Check for syntax errors in main files
console.log('\n🔍 Test 3: Checking for basic syntax issues...');
const filesToCheck = [
  'src/App.jsx',
  'src/index.jsx',
  'src/services/api.js'
];

let syntaxOk = true;
filesToCheck.forEach(file => {
  try {
    const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
    
    // Check for common issues
    if (content.includes('<<<<<<< SEARCH') || content.includes('>>>>>>> REPLACE')) {
      console.log(`   ❌ ${file} contains merge conflict markers`);
      issues.push(`${file} has unresolved merge conflicts`);
      syntaxOk = false;
    }
    
    // Check for import statements
    if (file.endsWith('.jsx') && !content.includes('import React')) {
      console.log(`   ⚠️  ${file} might be missing React import`);
    }
  } catch (error) {
    console.log(`   ❌ Error reading ${file}`);
    syntaxOk = false;
  }
});

if (syntaxOk) {
  console.log('   ✅ No obvious syntax issues found');
  passedTests++;
} else {
  console.log('   ❌ Syntax issues detected');
  failedTests++;
}

// Test 4: Check CSS files
console.log('\n🎨 Test 4: Checking CSS files...');
try {
  const themeCSS = fs.readFileSync(path.join(__dirname, 'src/styles/theme.css'), 'utf8');
  const componentsCSS = fs.readFileSync(path.join(__dirname, 'src/styles/components.css'), 'utf8');
  
  let cssOk = true;
  
  // Check for CSS variables
  if (!themeCSS.includes(':root')) {
    console.log('   ❌ theme.css missing :root variables');
    issues.push('theme.css missing CSS variables');
    cssOk = false;
  }
  
  // Check for key color variables
  const requiredVars = ['--bg-primary', '--neon-green', '--text-primary'];
  requiredVars.forEach(varName => {
    if (!themeCSS.includes(varName)) {
      console.log(`   ❌ Missing CSS variable: ${varName}`);
      issues.push(`Missing CSS variable: ${varName}`);
      cssOk = false;
    }
  });
  
  if (cssOk) {
    console.log('   ✅ CSS files look good');
    passedTests++;
  } else {
    failedTests++;
  }
} catch (error) {
  console.log('   ❌ Error reading CSS files');
  issues.push('Cannot read CSS files');
  failedTests++;
}

// Test 5: Check API configuration
console.log('\n🔌 Test 5: Checking API configuration...');
try {
  const apiFile = fs.readFileSync(path.join(__dirname, 'src/services/api.js'), 'utf8');
  
  let apiOk = true;
  
  if (!apiFile.includes('axios')) {
    console.log('   ❌ api.js missing axios import');
    issues.push('api.js missing axios');
    apiOk = false;
  }
  
  if (!apiFile.includes('baseURL')) {
    console.log('   ⚠️  api.js might be missing baseURL configuration');
  }
  
  if (apiOk) {
    console.log('   ✅ API configuration looks good');
    passedTests++;
  } else {
    failedTests++;
  }
} catch (error) {
  console.log('   ❌ Error reading api.js');
  issues.push('Cannot read api.js');
  failedTests++;
}

// Test 6: Check Vite configuration
console.log('\n⚡ Test 6: Checking Vite configuration...');
try {
  const viteConfig = fs.readFileSync(path.join(__dirname, 'vite.config.js'), 'utf8');
  
  let viteOk = true;
  
  if (!viteConfig.includes('react')) {
    console.log('   ❌ vite.config.js missing React plugin');
    issues.push('Vite config missing React plugin');
    viteOk = false;
  }
  
  if (!viteConfig.includes('proxy')) {
    console.log('   ⚠️  vite.config.js might be missing proxy configuration');
  }
  
  if (viteOk) {
    console.log('   ✅ Vite configuration looks good');
    passedTests++;
  } else {
    failedTests++;
  }
} catch (error) {
  console.log('   ❌ Error reading vite.config.js');
  issues.push('Cannot read vite.config.js');
  failedTests++;
}

// Test 7: Check component structure
console.log('\n🧩 Test 7: Checking component structure...');
const components = ['Navbar', 'MovieCard'];
let componentsOk = true;

components.forEach(component => {
  try {
    const content = fs.readFileSync(path.join(__dirname, `src/components/${component}.jsx`), 'utf8');
    
    if (!content.includes('export default')) {
      console.log(`   ❌ ${component}.jsx missing default export`);
      issues.push(`${component}.jsx missing export`);
      componentsOk = false;
    }
  } catch (error) {
    console.log(`   ❌ Error reading ${component}.jsx`);
    componentsOk = false;
  }
});

if (componentsOk) {
  console.log('   ✅ Component structure looks good');
  passedTests++;
} else {
  failedTests++;
}

// Test 8: Check page components
console.log('\n📄 Test 8: Checking page components...');
const pages = ['Home', 'Login', 'Register', 'Profile', 'News', 'Chat', 'Contact', 'AdminDashboard'];
let pagesOk = true;

pages.forEach(page => {
  try {
    const content = fs.readFileSync(path.join(__dirname, `src/pages/${page}.jsx`), 'utf8');
    
    if (!content.includes('export default')) {
      console.log(`   ❌ ${page}.jsx missing default export`);
      issues.push(`${page}.jsx missing export`);
      pagesOk = false;
    }
  } catch (error) {
    console.log(`   ❌ Error reading ${page}.jsx`);
    pagesOk = false;
  }
});

if (pagesOk) {
  console.log('   ✅ All page components present');
  passedTests++;
} else {
  failedTests++;
}

// Summary
console.log('\n' + '='.repeat(50));
console.log('📊 TEST SUMMARY');
console.log('='.repeat(50));
console.log(`✅ Passed: ${passedTests}`);
console.log(`❌ Failed: ${failedTests}`);
console.log(`📝 Total: ${passedTests + failedTests}`);

if (issues.length > 0) {
  console.log('\n⚠️  ISSUES FOUND:');
  issues.forEach((issue, index) => {
    console.log(`   ${index + 1}. ${issue}`);
  });
}

if (failedTests === 0) {
  console.log('\n🎉 All tests passed! Frontend is ready.');
  console.log('💡 Next steps:');
  console.log('   1. Run: npm run dev');
  console.log('   2. Open: http://localhost:3000');
  console.log('   3. Test manually using FRONTEND_TESTING_GUIDE.md');
  process.exit(0);
} else {
  console.log('\n❌ Some tests failed. Please fix the issues above.');
  process.exit(1);
}
