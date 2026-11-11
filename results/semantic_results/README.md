# Wyniki analizy semantycznej

Ten katalog zawiera tekstowy raport z analizy rzeczowników przy użyciu samoorganizującej się mapy Kohonena (SOM). Program i dane wejściowe są opisane w [`src/semantic_analysis/README.md`](../../src/semantic_analysis/README.md).

## Pliki wynikowe

| Plik | Działanie i zawartość | Źródło / powiązania |
|---|---|---|
| [`semantic_analysis.txt`](semantic_analysis.txt) | Raport tekstowy z liczbą analizowanych rzeczowników i czasowników, liczbą pustych neuronów, liczbą zidentyfikowanych pól semantycznych oraz globalną czystością klastrów. Zawiera też zestawienie niepustych neuronów: ich współrzędne na siatce, liczebność, dominującą kategorię, czystość i do 10 przykładowych rzeczowników. | Generuje go [`main.py`](../../src/semantic_analysis/main.py), korzystając z kategorii i leksykonu z [`vocabulary.py`](../../src/semantic_analysis/vocabulary.py). |
| [`README.md`](README.md) | Ten dokument - opisuje plik wynikowy i prowadzi do powiązanych plików źródłowych. | Dokumentacja kodu: [`src/semantic_analysis/README.md`](../../src/semantic_analysis/README.md). |

## Interpretacja

- Każdy neuron opisany w raporcie zawiera rzeczowniki przypisane do niego przez wyszukiwanie najlepiej dopasowanego neuronu (BMU).
- „Pole” i „czystość” klastra są wyznaczane na podstawie kategorii rzeczowników z [`vocabulary.py`](../../src/semantic_analysis/vocabulary.py); czystość to udział rzeczowników dominującej kategorii w danym klastrze.
- Lista rzeczowników przy neuronach jest skrócona do pierwszych 10 elementów; liczebność `n` dotyczy całego klastra.
- Raport odpowiada ostatniemu uruchomieniu programu i może się zmienić po ponownym wygenerowaniu.

## Powiązane katalogi i pliki

- Katalog wyników: [`results/semantic_results/`](./).
- Katalog implementacji: [`src/semantic_analysis/`](../../src/semantic_analysis/).
