<script lang="ts">

</script>

<div class="canvas">
  <div class="blind">
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
    transform: skewY(30deg);

    &::after {
      content: "";
      display: inline-block;
      height: 32px;
      width: 256px;
      border: 2px #444 solid;
      transform: skewX(-45deg) translateY(-36px) translateX(-21px);
    }
  }
</style>