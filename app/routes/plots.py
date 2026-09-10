from flask import Blueprint, request, jsonify
from ..models.plot import Plot
from .. import db
from ..utils.auth import token_required
from datetime import datetime

plots_bp = Blueprint('plots', __name__)

@plots_bp.route('', methods=['GET'])
@token_required
def get_plots(current_user):
    """List all plots"""
    plots = Plot.query.all()
    return jsonify([p.to_dict() for p in plots]), 200

@plots_bp.route('/<int:plot_id>', methods=['GET'])
@token_required
def get_plot(current_user, plot_id):
    """Get one plot by ID"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': 'Plot not found'}), 404
    return jsonify(plot.to_dict()), 200

@plots_bp.route('', methods=['POST'])
@token_required
def create_plot(current_user):
    """Create a new plot"""
    data = request.get_json()
    if not data.get('name'):
        return jsonify({'message': 'Plot name is required'}), 400

    plot = Plot(
        name=data['name'],
        grid_ref=data.get('grid_ref'),
        dimensions=data.get('dimensions'),
        soil_type=data.get('soil_type')
    )
    db.session.add(plot)
    db.session.commit()
    return jsonify(plot.to_dict()), 201

@plots_bp.route('/<int:plot_id>', methods=['PUT'])
@token_required
def update_plot(current_user, plot_id):
    """Update an existing plot"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': 'Plot not found'}), 404

    data = request.get_json()
    plot.name = data.get('name', plot.name)
    plot.grid_ref = data.get('grid_ref', plot.grid_ref)
    plot.dimensions = data.get('dimensions', plot.dimensions)
    plot.soil_type = data.get('soil_type', plot.soil_type)

    db.session.commit()
    return jsonify(plot.to_dict()), 200

@plots_bp.route('/<int:plot_id>', methods=['DELETE'])
@token_required
def delete_plot(current_user, plot_id):
    """Delete a plot"""
    plot = Plot.query.get(plot_id)
    if not plot:
        return jsonify({'message': 'Plot not found'}), 404

    db.session.delete(plot)
    db.session.commit()
    return jsonify({'message': 'Plot deleted successfully'}), 200