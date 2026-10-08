<script type="text/javascript">
$(document).ready(function() {  
   $('#pluginconfigboxharvester').hide(); 
});
</script>

<script type="text/javascript">
function showharvesterconfig()
{
   hideconfigs();
   
   $('#pluginconfigboxharvester').fadeIn(1000).show();
}
</script>

         <!--     PLUGIN ICONS     -->
      <a href = "#harvester">
      <div onclick = "showharvesterconfig()" id = "plugin" name = "{{plugin}}">
      <img src = "/static/images/plugins/harvester.png"><br>
      Credential Harvester
      </div>
      </a>
{# Reviewed 2026-10-08: archived Django UI, not loaded by the Python 3 package. #}
