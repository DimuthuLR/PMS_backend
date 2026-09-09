from flask import Blueprint, request, jsonify
from ..models import Plot
from .. import db
from ..utils.auth import token_required, admin_required

plots_bp = Blueprint('plots', __name__)

@plots_bp.route('', methods=['GET'])
@token_required
def get_plots():
    plots = Plot.query.all()
    return jsonify([p.to_dict() for p in plots]), 200

@plots_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_plot(id):
    plot = Plot.query.get(id)
    if not plot:
        return jsonify({'error': 'Plot not found'}), 404
    return jsonify(plot.to_dict()), 200

@plots_bp.route('', methods=['POST'])
@token_required
@admin_required
def create_plot():
    data = request.get_json()
    plot = Plot(
        name=data.get('name'),
        grid_ref=data.get('gridRef'),
        dimensions=data.get('dimensions'),
        soil_type=data.get('soilType')
    )
    db.session.add(plot)
    db.session.commit()
    return jsonify(plot.to_dict()), 201

@plots_bp.route('/<int:id>', methods=['PUT'])
@token_required
@admin_required
def update_plot(id):
    plot = Plot.query.get(id)
    if not plot:
        return jsonify({'error': 'Plot not found'}), 404
    data = request.get_json()
    plot.name = data.get('name', plot.name)
    plot.grid_ref = data.get('gridRef', plot.grid_ref)
    plot.dimensions = data.get('dimensions', plot.dimensions)
    plot.soil_type = data.get('soilType', plot.soil_type)
    db.session.commit()
    return jsonify(plot.to_dict()), 200

@plots_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@admin_required
def delete_plot(id):
    plot = Plot.query.get(id)
    if not plot:
        return jsonify({'error': 'Plot not found'}), 404
    db.session.delete(plot)
    db.session.commit()
    return jsonify({'message': 'Plot deleted'}), 200