import { defineConfig } from "vitepress"

export default defineConfig({
  title: "pyfplib",
  description: "Rust-inspired functional programming for Python — Option, Result, and functional helpers.",
  srcDir: "src",
  outDir: "dist",
  base: "/pyfplib/",

  locales: {
    root: {
      label: "English",
      lang: "en",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/guide/", activeMatch: "/guide/" },
          { text: "Option API", link: "/guide/option", activeMatch: "/guide/option" },
          { text: "Result API", link: "/guide/result", activeMatch: "/guide/result" },
          { text: "Functions API", link: "/guide/functools", activeMatch: "/guide/functools" },
        ],
        sidebar: [
          {
            text: "Introduction",
            items: [
              { text: "What is pyfplib?", link: "/guide/" },
              { text: "Getting Started", link: "/guide/getting-started" },
            ],
          },
          {
            text: "API Reference",
            items: [
              { text: "Option", link: "/guide/option" },
              { text: "Result", link: "/guide/result" },
              { text: "Functions", link: "/guide/functools" },
            ],
          },
        ],
      },
    },
    ru: {
      label: "Русский",
      lang: "ru",
      themeConfig: {
        nav: [
          { text: "Руководство", link: "/ru/guide/", activeMatch: "/ru/guide/" },
          { text: "API Option", link: "/ru/guide/option", activeMatch: "/ru/guide/option" },
          { text: "API Result", link: "/ru/guide/result", activeMatch: "/ru/guide/result" },
          { text: "API функций", link: "/ru/guide/functools", activeMatch: "/ru/guide/functools" },
        ],
        sidebar: [
          {
            text: "Введение",
            items: [
              { text: "Что такое pyfplib?", link: "/ru/guide/" },
              { text: "Начало работы", link: "/ru/guide/getting-started" },
            ],
          },
          {
            text: "Справочник API",
            items: [
              { text: "Option", link: "/ru/guide/option" },
              { text: "Result", link: "/ru/guide/result" },
              { text: "Функции", link: "/ru/guide/functools" },
            ],
          },
        ],
      },
    },
    zh: {
      label: "简体中文",
      lang: "zh-Hans",
      themeConfig: {
        nav: [
          { text: "指南", link: "/zh/guide/", activeMatch: "/zh/guide/" },
          { text: "Option API", link: "/zh/guide/option", activeMatch: "/zh/guide/option" },
          { text: "Result API", link: "/zh/guide/result", activeMatch: "/zh/guide/result" },
          { text: "函数 API", link: "/zh/guide/functools", activeMatch: "/zh/guide/functools" },
        ],
        sidebar: [
          {
            text: "介绍",
            items: [
              { text: "什么是 pyfplib？", link: "/zh/guide/" },
              { text: "快速开始", link: "/zh/guide/getting-started" },
            ],
          },
          {
            text: "API 参考",
            items: [
              { text: "Option", link: "/zh/guide/option" },
              { text: "Result", link: "/zh/guide/result" },
              { text: "函数", link: "/zh/guide/functools" },
            ],
          },
        ],
      },
    },
    de: {
      label: "Deutsch",
      lang: "de",
      themeConfig: {
        nav: [
          { text: "Handbuch", link: "/de/guide/", activeMatch: "/de/guide/" },
          { text: "Option-API", link: "/de/guide/option", activeMatch: "/de/guide/option" },
          { text: "Result-API", link: "/de/guide/result", activeMatch: "/de/guide/result" },
          { text: "Funktions-API", link: "/de/guide/functools", activeMatch: "/de/guide/functools" },
        ],
        sidebar: [
          {
            text: "Einführung",
            items: [
              { text: "Was ist pyfplib?", link: "/de/guide/" },
              { text: "Erste Schritte", link: "/de/guide/getting-started" },
            ],
          },
          {
            text: "API-Referenz",
            items: [
              { text: "Option", link: "/de/guide/option" },
              { text: "Result", link: "/de/guide/result" },
              { text: "Funktionen", link: "/de/guide/functools" },
            ],
          },
        ],
      },
    },
    it: {
      label: "Italiano",
      lang: "it",
      themeConfig: {
        nav: [
          { text: "Guida", link: "/it/guide/", activeMatch: "/it/guide/" },
          { text: "API Option", link: "/it/guide/option", activeMatch: "/it/guide/option" },
          { text: "API Result", link: "/it/guide/result", activeMatch: "/it/guide/result" },
          { text: "API Funzioni", link: "/it/guide/functools", activeMatch: "/it/guide/functools" },
        ],
        sidebar: [
          {
            text: "Introduzione",
            items: [
              { text: "Cos'è pyfplib?", link: "/it/guide/" },
              { text: "Per Iniziare", link: "/it/guide/getting-started" },
            ],
          },
          {
            text: "Riferimento API",
            items: [
              { text: "Option", link: "/it/guide/option" },
              { text: "Result", link: "/it/guide/result" },
              { text: "Funzioni", link: "/it/guide/functools" },
            ],
          },
        ],
      },
    },
    fr: {
      label: "Français",
      lang: "fr",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/fr/guide/", activeMatch: "/fr/guide/" },
          { text: "API Option", link: "/fr/guide/option", activeMatch: "/fr/guide/option" },
          { text: "API Result", link: "/fr/guide/result", activeMatch: "/fr/guide/result" },
          { text: "API Fonctions", link: "/fr/guide/functools", activeMatch: "/fr/guide/functools" },
        ],
        sidebar: [
          {
            text: "Introduction",
            items: [
              { text: "Qu'est-ce que pyfplib ?", link: "/fr/guide/" },
              { text: "Pour Commencer", link: "/fr/guide/getting-started" },
            ],
          },
          {
            text: "Référence API",
            items: [
              { text: "Option", link: "/fr/guide/option" },
              { text: "Result", link: "/fr/guide/result" },
              { text: "Fonctions", link: "/fr/guide/functools" },
            ],
          },
        ],
      },
    },
    pt: {
      label: "Português",
      lang: "pt",
      themeConfig: {
        nav: [
          { text: "Guia", link: "/pt/guide/", activeMatch: "/pt/guide/" },
          { text: "API de Option", link: "/pt/guide/option", activeMatch: "/pt/guide/option" },
          { text: "API de Result", link: "/pt/guide/result", activeMatch: "/pt/guide/result" },
          { text: "API de Funções", link: "/pt/guide/functools", activeMatch: "/pt/guide/functools" },
        ],
        sidebar: [
          {
            text: "Introdução",
            items: [
              { text: "O que é pyfplib?", link: "/pt/guide/" },
              { text: "Primeiros Passos", link: "/pt/guide/getting-started" },
            ],
          },
          {
            text: "Referência da API",
            items: [
              { text: "Option", link: "/pt/guide/option" },
              { text: "Result", link: "/pt/guide/result" },
              { text: "Funções", link: "/pt/guide/functools" },
            ],
          },
        ],
      },
    },
    ko: {
      label: "한국어",
      lang: "ko",
      themeConfig: {
        nav: [
          { text: "가이드", link: "/ko/guide/", activeMatch: "/ko/guide/" },
          { text: "Option API", link: "/ko/guide/option", activeMatch: "/ko/guide/option" },
          { text: "Result API", link: "/ko/guide/result", activeMatch: "/ko/guide/result" },
          { text: "함수 API", link: "/ko/guide/functools", activeMatch: "/ko/guide/functools" },
        ],
        sidebar: [
          {
            text: "소개",
            items: [
              { text: "pyfplib란?", link: "/ko/guide/" },
              { text: "시작하기", link: "/ko/guide/getting-started" },
            ],
          },
          {
            text: "API 레퍼런스",
            items: [
              { text: "Option", link: "/ko/guide/option" },
              { text: "Result", link: "/ko/guide/result" },
              { text: "함수", link: "/ko/guide/functools" },
            ],
          },
        ],
      },
    },
    ja: {
      label: "日本語",
      lang: "ja",
      themeConfig: {
        nav: [
          { text: "ガイド", link: "/ja/guide/", activeMatch: "/ja/guide/" },
          { text: "Option API", link: "/ja/guide/option", activeMatch: "/ja/guide/option" },
          { text: "Result API", link: "/ja/guide/result", activeMatch: "/ja/guide/result" },
          { text: "関数 API", link: "/ja/guide/functools", activeMatch: "/ja/guide/functools" },
        ],
        sidebar: [
          {
            text: "はじめに",
            items: [
              { text: "pyfplib とは？", link: "/ja/guide/" },
              { text: "セットアップ", link: "/ja/guide/getting-started" },
            ],
          },
          {
            text: "API リファレンス",
            items: [
              { text: "Option", link: "/ja/guide/option" },
              { text: "Result", link: "/ja/guide/result" },
              { text: "関数", link: "/ja/guide/functools" },
            ],
          },
        ],
      },
    },
    es: {
      label: "Español",
      lang: "es",
      themeConfig: {
        nav: [
          { text: "Guía", link: "/es/guide/", activeMatch: "/es/guide/" },
          { text: "API de Option", link: "/es/guide/option", activeMatch: "/es/guide/option" },
          { text: "API de Result", link: "/es/guide/result", activeMatch: "/es/guide/result" },
          { text: "API de Funciones", link: "/es/guide/functools", activeMatch: "/es/guide/functools" },
        ],
        sidebar: [
          {
            text: "Introducción",
            items: [
              { text: "¿Qué es pyfplib?", link: "/es/guide/" },
              { text: "Primeros Pasos", link: "/es/guide/getting-started" },
            ],
          },
          {
            text: "Referencia de la API",
            items: [
              { text: "Option", link: "/es/guide/option" },
              { text: "Result", link: "/es/guide/result" },
              { text: "Funciones", link: "/es/guide/functools" },
            ],
          },
        ],
      },
    },
  },

  head: [
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css",
      },
    ],
  ],

  themeConfig: {
    socialLinks: [{ icon: "github", link: "https://github.com/comet11x/pyfplib" }],
  },
})
