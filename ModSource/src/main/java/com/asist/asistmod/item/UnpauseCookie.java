package com.asist.asistmod.item;

import java.util.Arrays;

import com.asist.asistmod.missionhelpers.pause.PauseManager;

import net.minecraft.block.BlockContainer;
import net.minecraft.block.material.Material;
import net.minecraft.client.main.Main;
import net.minecraft.entity.EntityLivingBase;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.item.Item;
import net.minecraft.item.ItemAppleGold;
import net.minecraft.item.ItemFood;
import net.minecraft.item.ItemStack;
import net.minecraft.potion.PotionEffect;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;


public class UnpauseCookie extends ItemFood {
	
	public UnpauseCookie(String name) {
	    super(0, 0, false);
	    this.setUnlocalizedName(name);	    
	    this.setAlwaysEdible();
	}
	
	@Override
	protected void onFoodEaten(ItemStack stack, World worldIn, EntityPlayer player) {
		
		if(!worldIn.isRemote) {			
			PauseManager.unpauseMissionTimer();
			player.clearActivePotions();			
		}		
		
	}

}
