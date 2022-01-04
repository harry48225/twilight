<script lang="ts">
import { onMount } from "svelte";
type sunTimes = {
  'sunriseEnd': string,
  'goldenHourEnd': string,
  'dusk': string,
  'nightEnd': string,
  'night': string,
  'goldenHour': string,
  'sunset': string,
  'nauticalDawn': string,
  'sunsetStart': string,
  'dawn': string,
  'nauticalDusk': string,
  'sunrise': string
};

let times: sunTimes = undefined;

onMount(async () => {
  times = await (await fetch('/api/sun_times')).json();
  console.log(times)
});

const readableTime = (dateString: string) => {
  const date = new Date(dateString);
  return `${date.getHours().toString().padStart(2,'0')}:${date.getMinutes().toString().padStart(2,'0')}`}
</script>

<table>
  <tr>
    <th>nautical dawn</th>
    <th>dawn</th>
    <th>sunrise</th>
    <th>sunset</th>
    <th>dusk</th>
    <th>nautical dusk</th>
  </tr>
  <tr>
    {#if times}
      <td>{readableTime(times.nauticalDawn)}</td>
      <td>{readableTime(times.dawn)}</td>
      <td>{readableTime(times.sunrise)}</td>
      <td>{readableTime(times.sunset)}</td>
      <td>{readableTime(times.dusk)}</td>
      <td>{readableTime(times.nauticalDusk)}</td>
    {:else}
      <td>--:--</td>
      <td>--:--</td>
      <td>--:--</td>
      <td>--:--</td>
      <td>--:--</td>
      <td>--:--</td>
    {/if}
  </tr>
</table>

<style lang="scss">
  table {
    width: 100%;
    border-collapse: collapse;
    th, td {
    border: 1px #444 solid;
    padding: 8px;
    margin: 0px;
    }
  }
</style>