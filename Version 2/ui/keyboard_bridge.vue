<template>
  <div class="ase-keyboard-bridge" aria-hidden="true"></div>
</template>

<script>
module.exports = {
  mounted() {
    this._aseKeyHandler = (event) => {
      const tag = (event.target && event.target.tagName || "").toLowerCase();
      if (tag === "input" || tag === "textarea" || tag === "select") {
        return;
      }
      const mapping = {
        arrowup: "up",
        w: "up",
        arrowleft: "left",
        a: "left",
        arrowdown: "down",
        s: "down",
        arrowright: "right",
        d: "right",
      };
      const direction = mapping[String(event.key).toLowerCase()];
      if (!direction) {
        return;
      }
      event.preventDefault();
      this.event_key(direction);
    };
    document.addEventListener("keydown", this._aseKeyHandler);
  },
  beforeDestroy() {
    if (this._aseKeyHandler) {
      document.removeEventListener("keydown", this._aseKeyHandler);
    }
  },
};
</script>
