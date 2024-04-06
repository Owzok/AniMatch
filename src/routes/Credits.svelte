<script>
    let isOn = false;
  
    function toggleSwitch() {
      isOn = !isOn;
    }
  </script>
  
  <style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
    }

    .menu-toggle-container {
      position: relative;
      width: 60px;
      height: 30px;
      background-color: #ccc;
      border-radius: 15px;
      cursor: pointer;
    }
  
    .menu-toggle-handle {
      position: absolute;
      top: 0;
      left: 0;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background-color: white;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      transition: transform 0.3s ease-in-out;
    }
  
    .toggle-on {
      background-color: #4caf50 !important;
    }
  </style>
  
<div class:toggle-on={isOn} class="menu-toggle-container" on:click={toggleSwitch}>
    <div class="menu-toggle-handle" style="{isOn ? 'transform: translateX(30px)' : ''}"></div>
</div>

<h1>A</h1>

<h1>B</h1>

<h1>C</h1>