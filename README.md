import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Golf Game", layout="wide")

start = st.button("Start Game")

if start:
    GAME_HTML = r"""
    <!doctype html>
    <html>
    <head>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <style>
      html,body{margin:0;padding:0;height:100%;background:#76b852;overflow:hidden;}
      #gameCanvas{display:block;margin:0 auto;background:linear-gradient(#7ec850,#4aa02c);touch-action:none}
      #overlay{position:absolute;left:10px;top:10px;font-family:Arial,Helvetica,sans-serif;color:white;font-size:20px}
      #stopBtn{position:absolute;right:20px;top:20px;padding:10px 20px;background:black;color:white;border-radius:8px;cursor:pointer;font-family:Arial}
    </style>
    </head>
    <body>

    <canvas id=\"gameCanvas\"></canvas>
    <div id=\"overlay\"></div>
    <div id=\"stopBtn\">STOP</div>

    <script>
    (function(){
      const canvas = document.getElementById('gameCanvas');
      const ctx = canvas.getContext('2d');
      let DPR = window.devicePixelRatio||1;
      let canvasW, canvasH;

      const levels=[{},{},{}]; // 占位, 後面會用 resize 設定位置
      let levelIndex=0;
      let L={hole:{x:0,y:0}};
      let ball={x:0,y:0,r:10,vx:0,vy:0,moving:false};
      let strokes=0;
      let dragging=false;
      let dragStart=null;
      let endGame=false;

      function resize(){
        canvasW = Math.min(window.innerWidth,1400);
        canvasH = Math.min(window.innerHeight-20,800);
        canvas.style.width=canvasW+'px';
        canvas.style.height=canvasH+'px';
        canvas.width=Math.floor(canvasW*DPR);
        canvas.height=Math.floor(canvasH*DPR);
        ctx.setTransform(DPR,0,0,DPR,0,0);

        // 初始化或重新定位球與終點
        if(!ball.moving){
          ball.x = canvasW*0.15;
          ball.y = canvasH*0.5;
          L.hole.x = canvasW*0.85;
          L.hole.y = canvasH*0.5;
        }
      }
      window.addEventListener('resize',resize);
      resize();

      function updateOverlay(){
        const el=document.getElementById('overlay');
        if(endGame){el.innerHTML='All Levels Completed'; return;}
        el.innerHTML=`Level ${levelIndex+1}/2 &nbsp; Strokes: ${strokes}`;
      }

      function draw(){
        const w=canvas.width/DPR,h=canvas.height/DPR;
        ctx.clearRect(0,0,w,h);
        ctx.fillStyle='#7ec850';
        ctx.fillRect(0,0,w,h);

        // hole
        ctx.beginPath();
        ctx.fillStyle='black';
        ctx.arc(L.hole.x,L.hole.y,18,0,Math.PI*2);
        ctx.fill();

        // ball
        ctx.beginPath();
        ctx.fillStyle='white';
        ctx.arc(ball.x,ball.y,ball.r,0,Math.PI*2);
        ctx.fill();

        if(ball.moving){
          ball.x+=ball.vx;
          ball.y+=ball.vy;
          ball.vx*=0.9;
          ball.vy*=0.9;
          if(Math.hypot(ball.vx,ball.vy)<0.3){ball.vx=0;ball.vy=0;ball.moving=false;checkHole();}
        }

        requestAnimationFrame(draw);
      }

      function checkHole(){
        if(Math.hypot(ball.x-L.hole.x,ball.y-L.hole.y)<18){
          levelIndex++;
          if(levelIndex>=2){endGame=true; updateOverlay(); return;}
          // 重新設定球與終點
          ball.x = canvasW*0.15;
          ball.y = canvasH*0.5;
          L.hole.x = canvasW*0.85;
          L.hole.y = canvasH*0.5;
          ball.vx=0; ball.vy=0; ball.moving=false;
          strokes=0;
          updateOverlay();
        }
      }

      function startDrag(x,y){dragging=true; dragStart={x,y};}
      function endDrag(x,y){
        if(!dragging||endGame) return;
        dragging=false;
        strokes++;
        let dx=dragStart.x-x;
        let dy=dragStart.y-y;
        ball.vx=dx*0.2;
        ball.vy=dy*0.2;
        ball.moving=true;
        updateOverlay();
      }

      canvas.addEventListener('mousedown',e=>startDrag(e.offsetX,e.offsetY));
      canvas.addEventListener('mouseup',e=>endDrag(e.offsetX,e.offsetY));
      canvas.addEventListener('touchstart',e=>{
        const t=e.touches[0];
        startDrag(t.clientX-canvas.getBoundingClientRect().left,t.clientY-canvas.getBoundingClientRect().top);
      });
      canvas.addEventListener('touchend',e=>{
        const t=e.changedTouches[0];
        endDrag(t.clientX-canvas.getBoundingClientRect().left,t.clientY-canvas.getBoundingClientRect().top);
      });

      document.getElementById('stopBtn').onclick=()=>{ball.vx=0; ball.vy=0; ball.moving=false;};

      updateOverlay();
      draw();
    })();
    </script>
    </body>
    </html>
    """

    components.html(GAME_HTML,height=820,scrolling=False)
