package com.asist.asistmod.item;

import java.util.Arrays;

import net.minecraft.block.BlockContainer;
import net.minecraft.block.material.Material;
import net.minecraft.client.main.Main;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.Item;
import net.minecraft.item.ItemAppleGold;
import net.minecraft.item.ItemFood;
import net.minecraft.item.ItemPickaxe;
import net.minecraft.item.ItemStack;
import net.minecraft.potion.PotionEffect;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;


public class Stretcher extends ItemPickaxe {
	
	public Stretcher(String name, ToolMaterial material) {
		super(material);
	    this.setUnlocalizedName(name);	  
	}
}
