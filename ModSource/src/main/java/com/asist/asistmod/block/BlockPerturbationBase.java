package com.asist.asistmod.block;

import com.asist.asistmod.tile_entity.VictimBlockTileEntity;

import net.minecraft.block.BlockButton;
import net.minecraft.block.BlockContainer;
import net.minecraft.block.material.Material;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.EnumBlockRenderType;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

public class BlockPerturbationBase extends BlockContainer {
	
	public BlockPerturbationBase() {
		super(Material.GOURD);
	}

	
	@Override
	public EnumBlockRenderType getRenderType( IBlockState state) {
		return EnumBlockRenderType.MODEL;
	}
	
	@Override
	public TileEntity createNewTileEntity(World worldIn, int meta) {
		// TODO Auto-generated method stub
		return null;
	}
}
