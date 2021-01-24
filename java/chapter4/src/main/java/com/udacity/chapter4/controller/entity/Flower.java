package com.udacity.chapter4.controller.entity;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.hibernate.annotations.Nationalized;

import javax.persistence.*;
import java.math.BigDecimal;

@Entity
@Getter
@Setter
@NoArgsConstructor
@Table(name = "plant")
public class Flower {
    @Id
    @Setter(AccessLevel.PROTECTED)
    @GeneratedValue
    Long id;

    @Nationalized
    private String name;
    private String color;
    @Column(precision=12, scale=4)
    private BigDecimal price;

    public Flower(String name, String color, BigDecimal price) {
        this.name = name;
        this.color = color;
        this.price = price;
    }
}
