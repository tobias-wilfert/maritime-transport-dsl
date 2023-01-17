// base case; not stepped and no watercraft
var src="https://i.imgur.com/OK2FHgj.png";
if (getAttr("got_watercraft")){
  if (getAttr("has_stepped")){
    if (getAttr("got_this_turn")){
      src="https://i.imgur.com/CBU596h.png" // has NEW watercraft AND stepped
    }else{
      src="https://i.imgur.com/LZCToZI.png" // has OLD watercraft AND stepped
    }
  }else{
    src="https://i.imgur.com/2fZoJLC.png"; // has watercraft and NOT stepped
  }
}else if (getAttr("has_stepped")){
  src="https://i.imgur.com/vFzQR5X.png"; // has stepped and NO watercraft
}
({'src':src})