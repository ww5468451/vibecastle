document.addEventListener("DOMContentLoaded", () => {
    const svgNs = "http://www.w3.org/2000/svg";

    const animateBars = (scope) => {
        scope.querySelectorAll(".bar-fill").forEach((bar) => {
            bar.classList.remove("is-visible");
            const width = bar.dataset.width || "0";
            bar.style.setProperty("--bar-width", `${width}%`);
            window.requestAnimationFrame(() => {
                bar.classList.add("is-visible");
            });
        });
    };

    const initDeck = (deck) => {
        const buttons = Array.from(deck.querySelectorAll("[data-viz-button]"));
        const panels = Array.from(deck.querySelectorAll("[data-viz-panel]"));

        const setActive = (key) => {
            buttons.forEach((button) => {
                button.classList.toggle("active", button.dataset.vizButton === key);
            });

            panels.forEach((panel) => {
                const isActive = panel.dataset.vizPanel === key;
                panel.classList.toggle("active", isActive);
                if (isActive) {
                    animateBars(panel);
                }
            });
        };

        buttons.forEach((button) => {
            button.addEventListener("click", () => {
                setActive(button.dataset.vizButton);
            });
        });

        const initialKey = buttons.find((button) => button.classList.contains("active"))?.dataset.vizButton
            || buttons[0]?.dataset.vizButton;

        if (initialKey) {
            setActive(initialKey);
        }
    };

    const createSvg = (tag, attrs = {}) => {
        const node = document.createElementNS(svgNs, tag);
        Object.entries(attrs).forEach(([key, value]) => {
            node.setAttribute(key, String(value));
        });
        return node;
    };

    const readData = (sourceId) => {
        const source = document.getElementById(sourceId);
        if (!source) {
            return null;
        }

        try {
            return JSON.parse(source.textContent.trim());
        } catch (error) {
            console.error(`Unable to parse chart data for ${sourceId}`, error);
            return null;
        }
    };

    const setDetail = (sourceId, data, entry) => {
        const panel = document.querySelector(`[data-chart-detail="${sourceId}"]`);
        if (!panel || !entry) {
            return;
        }

        const chips = Object.entries(entry.meta || {})
            .map(([label, value]) => `<span class="meta-pill">${label}: ${value}</span>`)
            .join("");

        panel.classList.remove("is-empty");
        panel.innerHTML = `
            <p class="detail-kicker">${data.detailKicker || "Selected insight"}</p>
            <h3 class="detail-title">${entry.label}</h3>
            <p class="detail-copy">${entry.summary || ""}</p>
            <div class="detail-meta">${chips}</div>
        `;
    };

    const showTooltip = (tooltip, html, x, y, shell) => {
        tooltip.innerHTML = html;
        tooltip.classList.add("is-visible");

        const shellRect = shell.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        const left = Math.min(Math.max(12, x + 16), shellRect.width - tooltipRect.width - 12);
        const top = Math.min(Math.max(12, y - tooltipRect.height - 12), shellRect.height - tooltipRect.height - 12);

        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
    };

    const hideTooltip = (tooltip) => {
        tooltip.classList.remove("is-visible");
    };

    const tooltipHtml = (data, entry) => {
        const rows = [];
        rows.push(`<div class="tooltip-title">${entry.label}</div>`);
        rows.push(`<div class="tooltip-line">${data.xLabel}: ${entry.xLabel || entry.x}</div>`);
        rows.push(`<div class="tooltip-line">${data.yLabel}: ${entry.yLabel || entry.y}</div>`);
        if (entry.sizeLabel) {
            rows.push(`<div class="tooltip-line">${data.sizeLabel || "Size"}: ${entry.sizeLabel}</div>`);
        }
        return rows.join("");
    };

    const renderMatrixChart = (shell, sourceId, data) => {
        const width = 760;
        const height = 420;
        const padding = { top: 34, right: 28, bottom: 58, left: 62 };
        const innerWidth = width - padding.left - padding.right;
        const innerHeight = height - padding.top - padding.bottom;
        const xMin = data.xRange?.[0] ?? 0;
        const xMax = data.xRange?.[1] ?? 100;
        const yMin = data.yRange?.[0] ?? 0;
        const yMax = data.yRange?.[1] ?? 100;
        const xMid = data.xMid ?? (xMin + xMax) / 2;
        const yMid = data.yMid ?? (yMin + yMax) / 2;

        const scaleX = (value) => padding.left + ((value - xMin) / (xMax - xMin)) * innerWidth;
        const scaleY = (value) => padding.top + innerHeight - ((value - yMin) / (yMax - yMin)) * innerHeight;

        const svg = createSvg("svg", {
            viewBox: `0 0 ${width} ${height}`,
            class: "chart-svg",
            "aria-label": data.title || "interactive matrix chart"
        });

        for (let i = 0; i <= 4; i += 1) {
            const ratio = i / 4;
            const x = padding.left + ratio * innerWidth;
            const y = padding.top + ratio * innerHeight;

            svg.appendChild(createSvg("line", {
                x1: x,
                y1: padding.top,
                x2: x,
                y2: padding.top + innerHeight,
                class: "chart-grid-line"
            }));

            svg.appendChild(createSvg("line", {
                x1: padding.left,
                y1: y,
                x2: padding.left + innerWidth,
                y2: y,
                class: "chart-grid-line"
            }));
        }

        svg.appendChild(createSvg("line", {
            x1: padding.left,
            y1: padding.top + innerHeight,
            x2: padding.left + innerWidth,
            y2: padding.top + innerHeight,
            class: "chart-axis-line"
        }));
        svg.appendChild(createSvg("line", {
            x1: padding.left,
            y1: padding.top,
            x2: padding.left,
            y2: padding.top + innerHeight,
            class: "chart-axis-line"
        }));

        svg.appendChild(createSvg("line", {
            x1: scaleX(xMid),
            y1: padding.top,
            x2: scaleX(xMid),
            y2: padding.top + innerHeight,
            class: "chart-grid-line"
        }));
        svg.appendChild(createSvg("line", {
            x1: padding.left,
            y1: scaleY(yMid),
            x2: padding.left + innerWidth,
            y2: scaleY(yMid),
            class: "chart-grid-line"
        }));

        const xLabel = createSvg("text", {
            x: padding.left + innerWidth / 2,
            y: height - 14,
            "text-anchor": "middle",
            class: "chart-axis-text"
        });
        xLabel.textContent = data.xLabel;
        svg.appendChild(xLabel);

        const yLabel = createSvg("text", {
            x: 18,
            y: padding.top + innerHeight / 2,
            transform: `rotate(-90 18 ${padding.top + innerHeight / 2})`,
            "text-anchor": "middle",
            class: "chart-axis-text"
        });
        yLabel.textContent = data.yLabel;
        svg.appendChild(yLabel);

        (data.quadrants || []).forEach((item) => {
            const label = createSvg("text", {
                x: scaleX(item.x),
                y: scaleY(item.y),
                "text-anchor": item.align || "middle",
                class: "chart-quadrant"
            });
            label.textContent = item.label;
            svg.appendChild(label);
        });

        const tooltip = document.createElement("div");
        tooltip.className = "chart-tooltip";
        shell.innerHTML = "";
        shell.appendChild(svg);
        shell.appendChild(tooltip);

        const points = [];
        let activeCircle = null;

        const activate = (entry, circle, pointerEvent) => {
            if (activeCircle) {
                activeCircle.classList.remove("is-active");
            }
            activeCircle = circle;
            activeCircle.classList.add("is-active");
            setDetail(sourceId, data, entry);

            if (pointerEvent) {
                const shellRect = shell.getBoundingClientRect();
                showTooltip(
                    tooltip,
                    tooltipHtml(data, entry),
                    pointerEvent.clientX - shellRect.left,
                    pointerEvent.clientY - shellRect.top,
                    shell
                );
            }
        };

        data.series.forEach((entry, index) => {
            const cx = scaleX(entry.x);
            const cy = scaleY(entry.y);
            const r = entry.size || 18;

            const ring = createSvg("circle", {
                cx,
                cy,
                r: r + 5,
                class: "chart-point-ring"
            });
            svg.appendChild(ring);

            const circle = createSvg("circle", {
                cx,
                cy,
                r,
                fill: entry.color,
                class: "chart-point",
                tabindex: "0"
            });
            svg.appendChild(circle);

            const text = createSvg("text", {
                x: cx,
                y: cy + 4,
                "text-anchor": "middle",
                class: "matrix-label"
            });
            text.textContent = entry.shortLabel || entry.label;
            svg.appendChild(text);

            const onPointer = (event) => activate(entry, circle, event);

            circle.addEventListener("mouseenter", onPointer);
            circle.addEventListener("mousemove", onPointer);
            circle.addEventListener("focus", () => activate(entry, circle));
            circle.addEventListener("click", onPointer);
            circle.addEventListener("mouseleave", () => hideTooltip(tooltip));
            points.push({ circle, entry });

            if (index === 0) {
                activate(entry, circle);
            }
        });

        shell.addEventListener("mouseleave", () => hideTooltip(tooltip));
    };

    const renderRankChart = (shell, sourceId, data) => {
        const tooltip = document.createElement("div");
        tooltip.className = "chart-tooltip";
        shell.innerHTML = "";

        const wrapper = document.createElement("div");
        wrapper.className = "bar-list";
        shell.appendChild(wrapper);
        shell.appendChild(tooltip);

        const max = data.max || Math.max(...data.items.map((item) => item.value));
        let activeRow = null;

        data.items.forEach((item, index) => {
            const row = document.createElement("button");
            row.type = "button";
            row.className = "bar-row";
            row.innerHTML = `
                <div class="bar-meta"><span>${item.label}</span><span>${item.display || item.value}</span></div>
                <div class="bar-track"><span class="bar-fill" data-width="${(item.value / max) * 100}" style="--bar-color:${item.color};"></span></div>
            `;

            const activate = (event) => {
                if (activeRow) {
                    activeRow.classList.remove("is-active");
                }
                activeRow = row;
                activeRow.classList.add("is-active");
                setDetail(sourceId, data, item);

                if (event) {
                    const shellRect = shell.getBoundingClientRect();
                    showTooltip(
                        tooltip,
                        `<div class="tooltip-title">${item.label}</div><div class="tooltip-line">${data.valueLabel || "Value"}: ${item.display || item.value}</div>`,
                        event.clientX - shellRect.left,
                        event.clientY - shellRect.top,
                        shell
                    );
                }
            };

            row.addEventListener("mouseenter", activate);
            row.addEventListener("mousemove", activate);
            row.addEventListener("click", activate);
            row.addEventListener("mouseleave", () => hideTooltip(tooltip));
            wrapper.appendChild(row);

            if (index === 0) {
                activate();
            }
        });

        animateBars(wrapper);
    };

    const initCharts = () => {
        document.querySelectorAll("[data-chart][data-source]").forEach((shell) => {
            const chartType = shell.dataset.chart;
            const sourceId = shell.dataset.source;
            const data = readData(sourceId);

            if (!data) {
                return;
            }

            if (chartType === "matrix") {
                renderMatrixChart(shell, sourceId, data);
                return;
            }

            if (chartType === "rank") {
                renderRankChart(shell, sourceId, data);
            }
        });
    };

    document.querySelectorAll("[data-viz-deck]").forEach(initDeck);
    animateBars(document);
    initCharts();
});
