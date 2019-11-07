var dots;
var font;

function preload() {
  dots = loadImage("Win10LoadingDots.gif");
  font = loadFont('Segoe.ttf');
}

function setup() {
  //createCanvas(windowWidth, windowHeight);
  createCanvas(1920,1080);
  background(0, 120, 215);
  dots = createImg("Win10LoadingDots.gif");
  dots.size(200,AUTO);
  dots.position(width/2-100,height/2-90);
}

function draw() {
  background(0, 120, 215);
  let percentOfHour = floor(map(minute(), 0, 59, 0, 100));
  
  dots.size(200,AUTO);
  dots.position(windowWidth/2-100,windowHeight/2-90);
  
  textFont(font);
  textAlign(CENTER);
  textSize(28);
  fill(255);
  
  text("\n\nInstalling update " + hour() + " of 24\n" + percentOfHour + "% complete\nDo not turn off your computer",windowWidth/2-250,windowHeight/2-20,500,300);
  
}