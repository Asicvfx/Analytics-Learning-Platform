<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart, LineChart, PieChart } from "echarts/charts";
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from "echarts/components";
import VChart from "vue-echarts";
import type { ChartBlock } from "~/types";

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
]);

const props = defineProps<{ chart: ChartBlock }>();

const palette = ["#0A84FF", "#25D9FF", "#0057D9", "#10B981", "#F59E0B"];

const option = computed(() => {
  const labels = props.chart.data.map((d) => d.label);
  const values = props.chart.data.map((d) => d.value);

  if (props.chart.type === "PIE_CHART") {
    return {
      tooltip: { trigger: "item" },
      legend: { bottom: 0, textStyle: { color: "#64748B" } },
      color: palette,
      series: [
        {
          type: "pie",
          radius: ["45%", "70%"],
          data: props.chart.data.map((d) => ({ name: d.label, value: d.value })),
        },
      ],
    };
  }

  return {
    tooltip: { trigger: "axis" },
    grid: { left: 50, right: 20, top: 20, bottom: 40 },
    color: palette,
    xAxis: {
      type: "category",
      data: labels,
      axisLabel: { color: "#64748B", rotate: labels.length > 6 ? 30 : 0 },
    },
    yAxis: { type: "value", axisLabel: { color: "#64748B" } },
    series: [
      {
        type: props.chart.type === "LINE_CHART" ? "line" : "bar",
        data: values,
        smooth: true,
        itemStyle: { borderRadius: [6, 6, 0, 0] },
      },
    ],
  };
});
</script>

<template>
  <div class="card p-5">
    <h3 class="font-semibold text-ink mb-3">{{ chart.title }}</h3>
    <VChart :option="option" autoresize class="h-72 w-full" />
  </div>
</template>
