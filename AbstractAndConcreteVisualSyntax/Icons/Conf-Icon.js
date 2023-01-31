// base case 0 - no WC not stepped not new,mode 0
var src="https://i.imgur.com/sUnpybU.png";
if (getAttr("last_direction")){ // if TRUE mode is 1 (orange arrow)
    src="https://i.imgur.com/qbbDu2J.png";
    if (getAttr("got_watercraft")){
        if (getAttr("has_stepped")){
          if (getAttr("got_this_turn")){
            src="https://i.imgur.com/i8ER886.png" // has NEW watercraft AND stepped
          }else{
            src="https://i.imgur.com/hQhRArx.png" // has OLD watercraft AND stepped
          }
        }else{
          src="https://i.imgur.com/BqgQ5fd.png"; // has watercraft and NOT stepped
        }
    }else if (getAttr("has_stepped")){
        src="https://i.imgur.com/siQUwKK.png"; // has stepped and NO watercraft
    }
}else{ // ELSE mode is 0 (blue arrow)
    if (getAttr("got_watercraft")){
        if (getAttr("has_stepped")){
          if (getAttr("got_this_turn")){
            src="https://i.imgur.com/JBsSLYE.png" // has NEW watercraft AND stepped
          }else{
            src="https://i.imgur.com/cnxesKa.png" // has OLD watercraft AND stepped
          }
        }else{
          src="https://i.imgur.com/Bea57AF.png"; // has watercraft and NOT stepped
        }
    }else if (getAttr("has_stepped")){
        src="https://i.imgur.com/RBkyITy.png"; // has stepped and NO watercraft
    }
}
({'src':src})