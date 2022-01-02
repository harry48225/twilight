<script lang="ts">
  type sunTimes = {
    'sunriseEnd': Date,
    'goldenHourEnd': Date,
    'dusk': Date,
    'nightEnd': Date,
    'night': Date,
    'goldenHour': Date,
    'sunset': Date,
    'nauticalDawn': Date,
    'sunsetStart': Date,
    'dawn': Date,
    'nauticalDusk': Date,
    'sunrise': Date
  };
  export const times: sunTimes = {
    'sunriseEnd': new Date('2017-09-06 06:48:24'), 
    'goldenHourEnd': new Date('2017-09-06 07:20:27'), 
    'dusk': new Date('2017-09-06 19:59:44'), 
    'nightEnd': new Date('2017-09-06 05:15:09'), 
    'night': new Date('2017-09-06 21:03:39'), 
    'goldenHour': new Date('2017-09-06 18:58:21'), 
    'sunset': new Date('2017-09-06 19:33:08'), 
    'nauticalDawn': new Date('2017-09-06 05:47:35'), 
    'sunsetStart': new Date('2017-09-06 19:30:24'), 
    'dawn': new Date('2017-09-06 06:19:04'), 
    'nauticalDusk': new Date('2017-09-06 20:31:13'), 
    'sunrise': new Date('2017-09-06 06:45:40')
  };

  const readableTime = (date: Date) => `${date.getHours().toString().padStart(2,'0')}:${date.getMinutes().toString().padStart(2,'0')}`
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
    <td>{readableTime(times.nauticalDawn)}</td>
    <td>{readableTime(times.dawn)}</td>
    <td>{readableTime(times.sunrise)}</td>
    <td>{readableTime(times.sunset)}</td>
    <td>{readableTime(times.dusk)}</td>
    <td>{readableTime(times.nauticalDusk)}</td>
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