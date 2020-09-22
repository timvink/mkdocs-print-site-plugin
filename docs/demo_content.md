# Demo Content

This content is here to demonstrate what it looks like while printing.

:point_right: Go ahead and visit the [print page](print_page.html) and check it out!

## Links to other pages

`mkdocs-print-site-plugin` will fix internal links when combining all the pages into one. Try navigating to other site pages using these internal links:

- [Home](index.md)
- [Options](options.md)
- [Contributing](contributing.md)

## Links to other sections

When combining all pages into one, `mkdocs-print-site-plugin` will also ensure anchor links keep working (also to anchor links on other pages). Try them out:

- [Dummy section](#dummy-section) lower down this demo page
- The [Manual Testing](contributing.md#manual-testing) in the contributing guide

## Markdown extensions

MkDocs has support for many markdown extensions (see [mkdocs-material reference](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)). Below is a quick showcase so you can see how they print.

!!! note "Phasellus posuere in sem ut cursus"
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note ""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

!!! note
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

    ``` python
    def bubble_sort(items):
        for i in range(len(items)):
            for j in range(len(items) - 1 - i):
                if items[j] > items[j + 1]:
                    items[j], items[j + 1] = items[j + 1], items[j]
    ```

    Nunc eu odio eleifend, blandit leo a, volutpat sapien. Phasellus posuere in
    sem ut cursus. Nullam sit amet tincidunt ipsum, sit amet elementum turpis.
    Etiam ipsum quam, mattis in purus vitae, lacinia fermentum enim.

??? note
    This is a collapsible block, that is collapsed by default.

[Example of a button](#){: .md-button }

[Primary button](#){: .md-button .md-button--primary }

[With icon :fontawesome-solid-paper-plane:](#){: .md-button .md-button--primary }

``` python
import tensorflow as tf
```

``` python linenums="1"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

``` python hl_lines="2 3"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

The `#!python range()` function is used to generate a sequence of numbers.

++ctrl+alt+del++

=== "C"

    ``` c
    #include <stdio.h>

    int main(void) {
      printf("Hello world!\n");
      return 0;
    }
    ```

=== "C++"

    ``` c++
    #include <iostream>

    int main(void) {
      std::cout << "Hello world!" << std::endl;
      return 0;
    }
    ```

Another tabbed content

=== "Unordered list"

    * Sed sagittis eleifend rutrum
    * Donec vitae suscipit est
    * Nulla tempor lobortis orci

=== "Ordered list"

    1. Sed sagittis eleifend rutrum
    2. Donec vitae suscipit est
    3. Nulla tempor lobortis orci

Embedding content:

!!! example

    === "Unordered List"

        _Example_:

        ``` markdown
        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci
        ```

        _Result_:

        * Sed sagittis eleifend rutrum
        * Donec vitae suscipit est
        * Nulla tempor lobortis orci

    === "Ordered List"

        _Example_:

        ``` markdown
        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci
        ```

        _Result_:

        1. Sed sagittis eleifend rutrum
        2. Donec vitae suscipit est
        3. Nulla tempor lobortis orci

| Method      | Description                          |
| ----------- | ------------------------------------ |
| `GET`       | :material-check:     Fetch resource  |
| `PUT`       | :material-check-all: Update resource |
| `DELETE`    | :material-close:     Delete resource |

Lorem ipsum[^1] dolor sit amet, consectetur adipiscing elit.[^2]

[^1]: Lorem ipsum dolor sit amet, consectetur adipiscing elit.
[^2]:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla et euismod
    nulla. Curabitur feugiat, tortor non consequat finibus, justo purus auctor
    massa, nec semper lorem quam in massa.

* :material-account-circle: – `.icons/material/account-circle.svg`
* :fontawesome-regular-laugh-wink: – `.icons/fontawesome/regular/laugh-wink.svg`
* :octicons-octoface-16: – `.icons/octicons/octoface-16.svg`
* :fontawesome-brands-medium:{: .medium } – Medium
* :fontawesome-brands-twitter:{: .twitter } – Twitter
* :fontawesome-brands-facebook:{: .facebook } – Facebook

:smile: 

### Images

`mkdocs-print-site-plugin` supports enumerating figure captions (which can be added easily using the [img2fig](https://github.com/stuebersystems/mkdocs-img2fig-plugin) plugin):

<figure>
  <img src="https://dummyimage.com/600x400/eee/aaa" width="300" />
  <figcaption>Image caption</figcaption>
</figure>

<figure>
  <img src="https://dummyimage.com/600x400/eee/aaa" width="300" />
  <figcaption>Another image caption</figcaption>
</figure>

![](https://play-lh.googleusercontent.com/JHDqEqU0QNC8vsa5_UsPAws5X1OvTVPcfDVLnV1WXhoYrEX81sE6fL7cmamStPrK_A=w1440-h620-rw "A cat playing")

![](https://play-lh.googleusercontent.com/tKuOgQBwDTjhZg3DjCdZVTSVa9X9iMrtrM_1JDH6Ky_YyQeKw_bnFDy0tj1aZ39TDnI=w1440-h620-r "Another cat playing")

![](https://play-lh.googleusercontent.com/4CPahw1_E0b61tZKq4QI1bw_dqR6bYy0aDiNWrn-MCoz9Wq5bNyhKywfVlK01nNKR-A=w1440-h620-r "More cats that play")

![](https://play-lh.googleusercontent.com/5DeXBFITrh81XB68XxvJGvat5bwVj2ELVdSXNb6mGdvohZtnUoUl5kkPLPSrgtN9XHk=w1440-h620-r "The internet loves cats")


### Lists

1. Vivamus id mi enim. Integer id turpis sapien. Ut condimentum lobortis
  sagittis. Aliquam purus tellus, faucibus eget urna at, iaculis venenatis
  nulla. Vivamus a pharetra leo.

    1. Vivamus venenatis porttitor tortor sit amet rutrum. Pellentesque aliquet
      quam enim, eu volutpat urna rutrum a. Nam vehicula nunc mauris, a
      ultricies libero efficitur sed.

    2. Morbi eget dapibus felis. Vivamus venenatis porttitor tortor sit amet
      rutrum. Pellentesque aliquet quam enim, eu volutpat urna rutrum a.

        1. Mauris dictum mi lacus
        2. Ut sit amet placerat ante
        3. Suspendisse ac eros arcu

`Lorem ipsum dolor sit amet`
:   Sed sagittis eleifend rutrum. Donec vitae suscipit est. Nullam tempus
    tellus non sem sollicitudin, quis rutrum leo facilisis.

`Cras arcu libero`
:   Aliquam metus eros, pretium sed nulla venenatis, faucibus auctor ex. Proin
    ut eros sed sapien ullamcorper consequat. Nunc ligula ante.

    Duis mollis est eget nibh volutpat, fermentum aliquet dui mollis.
    Nam vulputate tincidunt fringilla.
    Nullam dignissim ultrices urna non auctor.

* [x] Lorem ipsum dolor sit amet, consectetur adipiscing elit
* [ ] Vestibulum convallis sit amet nisi a tincidunt
    * [x] In hac habitasse platea dictumst
    * [x] In scelerisque nibh non dolor mollis congue sed et metus
    * [ ] Praesent sed risus massa
* [ ] Aenean pretium efficitur erat, donec pharetra, ligula non scelerisque

$$
\operatorname{ker} f=\{g\in G:f(g)=e_{H}\}{\mbox{.}}
$$

The homomorphism $f$ is injective if and only if its kernel is only the 
singleton set $e_G$, because otherwise $\exists a,b\in G$ with $a\neq b$ such 
that $f(a)=f(b)$00.

## Dummy section

This section has an incoming anchor link, at the top of this page

## Some [lorem ipsum](https://www.lipsum.com/)

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut eget mi lacinia arcu ultrices rutrum eget a lacus. Etiam erat mi, sodales at nisl vel, bibendum tempor nunc. Cras in ultrices augue. Cras aliquam in mauris et semper. In hac habitasse platea dictumst. Proin dignissim scelerisque risus, consectetur ornare justo ultrices eu. Quisque tempus, elit eu ullamcorper interdum, metus augue pulvinar lectus, nec dictum mi dolor non turpis. Sed condimentum vulputate pretium.

Nulla at nisl tortor. Praesent vitae turpis sit amet sem condimentum fermentum eget nec dolor. Maecenas et imperdiet ante, at ultrices orci. Nunc ornare sodales enim. Sed tempor vitae mi et faucibus. Nunc aliquam est sit amet mauris tempus varius. Aenean blandit vel nibh nec sagittis. Sed vehicula nunc a nunc vehicula viverra. Proin risus justo, ullamcorper ac sem a, vulputate ornare justo. Sed facilisis pharetra elit, vitae dignissim nibh iaculis eu. Suspendisse potenti. Curabitur quis arcu ac est faucibus suscipit vel non lacus.

Ut tincidunt sapien sed sem auctor, et pellentesque erat tristique. Nunc porttitor lacus diam, eu malesuada nibh venenatis in. Donec sit amet enim eget enim facilisis placerat nec eget tortor. Etiam imperdiet, felis ac posuere dignissim, nulla sapien auctor mauris, ac aliquam orci leo nec dui. Donec efficitur turpis quis enim efficitur, eu ornare nisi consectetur. Sed ac arcu at orci pretium lobortis luctus non augue. Duis posuere purus at semper fringilla. Pellentesque facilisis libero vestibulum elit varius iaculis. Donec dapibus pretium scelerisque.

Suspendisse non orci vitae lorem placerat pretium vitae a ex. Nunc facilisis aliquam risus in vehicula. Fusce sodales bibendum lectus id ultricies. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In cursus blandit quam ac bibendum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Ut commodo tellus vel interdum vulputate. Nulla in turpis tellus. Mauris at semper ex. Nulla varius leo eu libero placerat, quis euismod orci euismod. Phasellus pulvinar ut sapien nec elementum. Maecenas vel mi eros. Interdum et malesuada fames ac ante ipsum primis in faucibus. Phasellus volutpat massa vel purus interdum imperdiet. Curabitur congue turpis eget faucibus varius. Aenean eleifend placerat lorem vel vestibulum.

Nullam in posuere urna. Sed cursus est porta maximus dignissim. Etiam id ante libero. Curabitur ac rhoncus turpis. Cras eu ipsum lacus. Aliquam ac rutrum elit. Donec pharetra in arcu feugiat interdum. Nam sed libero semper, sollicitudin urna vel, tincidunt nulla. Curabitur dapibus massa lectus, vulputate fermentum est finibus et. Ut efficitur velit nec justo varius tempor. Nullam aliquet commodo enim eget lobortis. Nullam sit amet nunc viverra, iaculis sem non, scelerisque mauris. Vivamus eu finibus lacus, dignissim luctus elit.