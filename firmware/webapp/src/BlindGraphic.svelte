<script lang="ts">
  import { tweened } from 'svelte/motion';
  const minHeight = 30;
  const maxHeight = 512;
  export let normalisedHeight: number; // Normalised

  const tweenedHeight = tweened(0, {
    duration: 5000,
    easing: (t) => Math.sin(-13.0 * (t + 1.0) * Math.PI/2) * Math.pow(2.0, -40.0 * t) + 1.0 // Tweaked elastic out
  })

  $: $tweenedHeight = minHeight + normalisedHeight * (maxHeight - minHeight);
</script>

<div class="canvas">
  <div class="blind" style={`height: ${Math.max($tweenedHeight,0)}px`}>
  </div>
</div>

<style lang="scss">
  .canvas {
    width: 100%;
    margin-top: 128px;
    
    > div {
      margin: 0 auto;
    }
  }

  .blind {
    height: 512px;
    width: 256px;
    border: 2px #444 solid;
    transform-style: preserve-3d;
    display: block;
    transform: skewY(30deg);
    background-color: #222;

    // Top of blind
    &::before {
      content: "";
      display: inline-block;
      height: 32px;
      width: 256px;
      border: 2px #444 solid;
      transform: skewX(-45deg) translateY(-36px) translateX(-21px);
    }

    // Window sill
    &::after {
      content:"";
      display: block;
      border: 2px #c8c8c8 solid;
      width: 320px;
      height: 64px;
      transform: skewX(-45deg) translateY(440px) translateX(408px) translateZ(-1px);
      
    }
  }
</style>