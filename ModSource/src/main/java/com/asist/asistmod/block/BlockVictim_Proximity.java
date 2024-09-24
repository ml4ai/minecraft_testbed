package com.asist.asistmod.block;

import java.util.Random;

import com.asist.asistmod.tile_entity.VictimBlockProximityTileEntity;

import net.minecraft.block.Block;
import net.minecraft.block.BlockContainer;
import net.minecraft.block.BlockDirt;
import net.minecraft.block.material.Material;
import net.minecraft.block.properties.IProperty;
import net.minecraft.block.properties.PropertyBool;
import net.minecraft.block.properties.PropertyInteger;
import net.minecraft.block.state.BlockStateContainer;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.Entity;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.EnumBlockRenderType;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class BlockVictim_Proximity extends BlockContainer {
	
	VictimBlockProximityTileEntity tileEntity;	
	public BlockVictim_Proximity() {
		super(Material.WOOD);
		this.setHardness(10f);
		this.setTickRandomly(true);	
		
	}
	
	@Override
	public TileEntity createNewTileEntity(World worldIn, int meta) {		
		tileEntity = new VictimBlockProximityTileEntity();			
		return tileEntity;
	}
	
	// MAKES THE RENDERER WORK, OTHERWISE BLOCK IS INVISIBLE
	@Override
	public EnumBlockRenderType getRenderType( IBlockState state) {
	  return EnumBlockRenderType.MODEL;
	}	
}
