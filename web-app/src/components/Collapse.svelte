<script>
    export let title;
    export let content;
</script>

<div class="collapse collapse-arrow">
    <input type="checkbox" /> 
    <div class="collapse-title font-medium text-lg">
      - {title}
    </div>
    <div class="collapse-content text-sm"> 
      <p class="ml-4">{content}</p>
    </div>
  </div>