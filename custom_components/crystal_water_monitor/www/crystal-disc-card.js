class CrystalDiscCard extends HTMLElement {
  static get properties() {
    return { hass: {}, config: {} };
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  setConfig(config) {
    if (!config.entity) throw new Error("Please define an entity (Water Status sensor)");
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  _getDisc() {
    if (!this._hass || !this._config) return null;
    const state = this._hass.states[this._config.entity];
    if (!state) return null;
    return state.attributes;
  }

  _colorForStatus(color) {
    return { blue: "#2d7fc1", orange: "#e07b39", red: "#c0392b", gray: "#666" }[color] || "#2d7fc1";
  }

  _render() {
    const disc = this._getDisc();
    if (!disc) {
      this.innerHTML = `<ha-card><div style="padding:16px">Entity not found</div></ha-card>`;
      return;
    }

    const color = this._hass.states[this._config.entity]?.attributes?.waterStatusColor || "blue";
    const bg = this._colorForStatus(color);
    const name = disc.name || "";
    const text = disc.text || "";
    const lastUpdated = disc.lastUpdatedText || "";
    const tempC = disc.tempC;
    const tempF = tempC != null ? ((tempC * 9) / 5 + 32).toFixed(0) : null;
    const temp = tempF != null ? `${tempF}°F` : "";

    this.innerHTML = `
      <ha-card>
        <div style="
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 24px;
        ">
          <div style="
            background: ${bg};
            clip-path: polygon(50% 0%, 93% 25%, 93% 75%, 50% 100%, 7% 75%, 7% 25%);
            width: 220px;
            height: 240px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
            padding: 32px;
            box-sizing: border-box;
          ">
            <div style="font-size: 14px; font-weight: 600; margin-bottom: 8px;">${name}</div>
            <div style="font-size: 48px; font-weight: 700; line-height: 1;">${temp}</div>
            <div style="font-size: 14px; margin-top: 8px;">${text}</div>
            <div style="font-size: 11px; margin-top: 12px; opacity: 0.8;">${lastUpdated}</div>
          </div>
        </div>
      </ha-card>
    `;
  }
}

customElements.define("crystal-disc-card", CrystalDiscCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "crystal-disc-card",
  name: "Crystal Disc",
  description: "Water status disc for Crystal Water Monitor",
});
