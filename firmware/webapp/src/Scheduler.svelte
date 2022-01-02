<script lang="ts">
  export let openTime: string = "sunrise";
  export let closeTime: string = "sunset";
</script>

<div>
  open at 
  <select bind:value={openTime}>
    <option>nautical dawn</option>
    <option>dawn</option>
    <option>sunrise</option>
  </select>, 
  and close at 
  <select bind:value={closeTime}>
    <option>sunset</option>
    <option>dusk</option>
    <option>nautical dusk</option>
  </select>
</div>

<style lang="scss">
  select {
    border-radius: 0px;
    border: none;
    text-align: center;
    background-color: #c8c8c8;
  }
</style>